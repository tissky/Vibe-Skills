param(
    [Parameter(Mandatory)] [string]$Task,
    [string]$Mode = 'interactive_governed',
    [string]$RunId = '',
    [string]$RequirementDocPath = '',
    [string]$ExecutionPlanPath = '',
    [string]$RuntimeInputPacketPath = '',
    [string]$ArtifactRoot = '',
    [AllowEmptyString()] [string]$GovernanceScope = '',
    [AllowEmptyString()] [string]$RootRunId = '',
    [AllowEmptyString()] [string]$ParentRunId = '',
    [AllowEmptyString()] [string]$ParentUnitId = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'VibeRuntime.Common.ps1')

function Expand-VibeExecutionTemplate {
    param(
        [AllowEmptyString()] [string]$Text,
        [hashtable]$Tokens
    )

    $value = if ($null -eq $Text) { '' } else { [string]$Text }
    foreach ($key in @($Tokens.Keys)) {
        $value = $value.Replace($key, [string]$Tokens[$key])
    }
    return $value
}

function Invoke-VibeCapturedProcess {
    param(
        [Parameter(Mandatory)] [string]$Command,
        [string[]]$Arguments = @(),
        [Parameter(Mandatory)] [string]$WorkingDirectory,
        [Parameter(Mandatory)] [int]$TimeoutSeconds,
        [Parameter(Mandatory)] [string]$StdOutPath,
        [Parameter(Mandatory)] [string]$StdErrPath
    )

    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $Command
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $quotedArguments = foreach ($argument in @($Arguments)) {
        $text = [string]$argument
        if ($text -match '[\s"]') {
            '"' + ($text -replace '"', '\"') + '"'
        } else {
            $text
        }
    }
    $startInfo.Arguments = [string]::Join(' ', @($quotedArguments))

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo

    try {
        if (-not $process.Start()) {
            throw "Failed to start process: $Command"
        }

        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()

        $timedOut = -not $process.WaitForExit($TimeoutSeconds * 1000)
        if ($timedOut) {
            try {
                $process.Kill($true)
            } catch {
            }
            $process.WaitForExit()
        }

        $stdoutText = $stdoutTask.GetAwaiter().GetResult()
        $stderrText = $stderrTask.GetAwaiter().GetResult()
        Write-VgoUtf8NoBomText -Path $StdOutPath -Content $stdoutText
        Write-VgoUtf8NoBomText -Path $StdErrPath -Content $stderrText

        return [pscustomobject]@{
            exit_code = if ($timedOut) { -1 } else { [int]$process.ExitCode }
            timed_out = [bool]$timedOut
            stdout_path = $StdOutPath
            stderr_path = $StdErrPath
            stdout_preview = (($stdoutText -split "`r?`n" | Where-Object { $_ -ne '' }) | Select-Object -First 5)
            stderr_preview = (($stderrText -split "`r?`n" | Where-Object { $_ -ne '' }) | Select-Object -First 5)
        }
    } finally {
        $process.Dispose()
    }
}

function Invoke-VibeExecutionUnit {
    param(
        [Parameter(Mandatory)] [object]$Unit,
        [Parameter(Mandatory)] [string]$RepoRoot,
        [Parameter(Mandatory)] [string]$SessionRoot,
        [Parameter(Mandatory)] [hashtable]$Tokens,
        [Parameter(Mandatory)] [int]$DefaultTimeoutSeconds
    )

    $logsRoot = Join-Path $SessionRoot 'execution-logs'
    $resultsRoot = Join-Path $SessionRoot 'execution-results'
    New-Item -ItemType Directory -Path $logsRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $resultsRoot -Force | Out-Null

    $unitId = [string]$Unit.unit_id
    $kind = [string]$Unit.kind
    $timeoutSeconds = if ($Unit.PSObject.Properties.Name -contains 'timeout_seconds' -and $null -ne $Unit.timeout_seconds) {
        [int]$Unit.timeout_seconds
    } else {
        [int]$DefaultTimeoutSeconds
    }
    $expectedExitCode = if ($Unit.PSObject.Properties.Name -contains 'expected_exit_code' -and $null -ne $Unit.expected_exit_code) {
        [int]$Unit.expected_exit_code
    } else {
        0
    }
    $cwd = Expand-VibeExecutionTemplate -Text ([string]$Unit.cwd) -Tokens $Tokens
    if ([string]::IsNullOrWhiteSpace($cwd)) {
        $cwd = $RepoRoot
    }
    if (-not [System.IO.Path]::IsPathRooted($cwd)) {
        $cwd = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $cwd))
    }

    $stdoutPath = Join-Path $logsRoot ("{0}.stdout.log" -f $unitId)
    $stderrPath = Join-Path $logsRoot ("{0}.stderr.log" -f $unitId)
    $startedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $command = ''
    $arguments = @()
    $display = ''

    switch ($kind) {
        'powershell_file' {
            $scriptPathRaw = Expand-VibeExecutionTemplate -Text ([string]$Unit.script_path) -Tokens $Tokens
            $scriptPath = if ([System.IO.Path]::IsPathRooted($scriptPathRaw)) {
                [System.IO.Path]::GetFullPath($scriptPathRaw)
            } else {
                [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $scriptPathRaw))
            }

            $args = @()
            foreach ($arg in @($Unit.arguments)) {
                $args += (Expand-VibeExecutionTemplate -Text ([string]$arg) -Tokens $Tokens)
            }

            $invocation = Get-VgoPowerShellFileInvocation -ScriptPath $scriptPath -ArgumentList $args -NoProfile
            $command = [string]$invocation.host_path
            $arguments = @($invocation.arguments)
            $display = @($command) + @($arguments) -join ' '
        }
        'python_command' {
            $commandSpec = Expand-VibeExecutionTemplate -Text ([string]$Unit.command) -Tokens $Tokens
            $pythonInvocation = Resolve-VgoPythonCommandSpec -Command $commandSpec
            $command = [string]$pythonInvocation.host_path
            $arguments = @($pythonInvocation.prefix_arguments)
            foreach ($arg in @($Unit.arguments)) {
                $arguments += (Expand-VibeExecutionTemplate -Text ([string]$arg) -Tokens $Tokens)
            }
            $display = @($command) + @($arguments) -join ' '
        }
        'shell_command' {
            $command = Expand-VibeExecutionTemplate -Text ([string]$Unit.command) -Tokens $Tokens
            foreach ($arg in @($Unit.arguments)) {
                $arguments += (Expand-VibeExecutionTemplate -Text ([string]$arg) -Tokens $Tokens)
            }
            $display = @($command) + @($arguments) -join ' '
        }
        default {
            throw "Unsupported benchmark execution unit kind: $kind"
        }
    }

    $processResult = Invoke-VibeCapturedProcess -Command $command -Arguments $arguments -WorkingDirectory $cwd -TimeoutSeconds $timeoutSeconds -StdOutPath $stdoutPath -StdErrPath $stderrPath

    $resolvedArtifacts = @()
    foreach ($artifact in @($Unit.expected_artifacts)) {
        $expanded = Expand-VibeExecutionTemplate -Text ([string]$artifact) -Tokens $Tokens
        $artifactPath = if ([System.IO.Path]::IsPathRooted($expanded)) {
            [System.IO.Path]::GetFullPath($expanded)
        } else {
            [System.IO.Path]::GetFullPath((Join-Path $cwd $expanded))
        }
        $resolvedArtifacts += [pscustomobject]@{
            path = $artifactPath
            exists = [bool](Test-Path -LiteralPath $artifactPath)
        }
    }

    $finishedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $verificationPassed = (-not $processResult.timed_out) -and ([int]$processResult.exit_code -eq $expectedExitCode) -and (@($resolvedArtifacts | Where-Object { -not $_.exists }).Count -eq 0)

    $unitResult = [pscustomobject]@{
        unit_id = $unitId
        kind = $kind
        status = if ($verificationPassed) { 'completed' } elseif ($processResult.timed_out) { 'timed_out' } else { 'failed' }
        started_at = $startedAt
        finished_at = $finishedAt
        command = $command
        arguments = @($arguments)
        display_command = $display
        cwd = $cwd
        timeout_seconds = $timeoutSeconds
        expected_exit_code = $expectedExitCode
        exit_code = [int]$processResult.exit_code
        timed_out = [bool]$processResult.timed_out
        stdout_path = $processResult.stdout_path
        stderr_path = $processResult.stderr_path
        stdout_preview = @($processResult.stdout_preview)
        stderr_preview = @($processResult.stderr_preview)
        expected_artifacts = @($resolvedArtifacts)
        verification_passed = [bool]$verificationPassed
    }

    $resultPath = Join-Path $resultsRoot ("{0}.json" -f $unitId)
    Write-VibeJsonArtifact -Path $resultPath -Value $unitResult

    return [pscustomobject]@{
        result = $unitResult
        result_path = $resultPath
    }
}

function Get-VibePlanSections {
    param(
        [Parameter(Mandatory)] [string]$PlanPath
    )

    $sections = [ordered]@{}
    $currentSection = '__preamble__'
    $sections[$currentSection] = [System.Collections.Generic.List[string]]::new()
    foreach ($line in @(Get-Content -LiteralPath $PlanPath -Encoding UTF8)) {
        if ($line -match '^##\s+(.*)$') {
            $currentSection = $Matches[1].Trim()
            if (-not $sections.Contains($currentSection)) {
                $sections[$currentSection] = [System.Collections.Generic.List[string]]::new()
            }
            continue
        }
        $sections[$currentSection].Add([string]$line) | Out-Null
    }

    return $sections
}

function Get-VibePlanDerivedExecutionShadow {
    param(
        [Parameter(Mandatory)] [string]$PlanPath,
        [Parameter(Mandatory)] [string]$RunId,
        [Parameter(Mandatory)] [string]$SessionRoot
    )

    $sections = Get-VibePlanSections -PlanPath $PlanPath
    $units = @()
    $sectionOrder = @('Wave Plan', 'Specialist Skill Dispatch Plan', 'Verification Commands', 'Phase Cleanup Contract')
    $unitIndex = 0

    foreach ($sectionName in $sectionOrder) {
        if (-not $sections.Contains($sectionName)) {
            continue
        }

        foreach ($line in @($sections[$sectionName])) {
            $trimmed = [string]$line.Trim()
            if (-not $trimmed.StartsWith('-')) {
                continue
            }

            $unitIndex += 1
            $classification = 'advisory_only_unit'
            $reason = 'narrative_bullet_without_executable_command'
            $inlineCommands = [regex]::Matches($trimmed, '`([^`]+)`') | ForEach-Object { $_.Groups[1].Value }

            if ($sectionName -eq 'Specialist Skill Dispatch Plan') {
                $classification = 'specialist_dispatch_unit'
                $reason = 'bounded_native_specialist_dispatch_declared'
            } elseif (@($inlineCommands).Count -gt 0) {
                $classification = 'executable_unit'
                $reason = 'inline_command_detected'
            } elseif ($sectionName -eq 'Verification Commands') {
                $classification = 'ambiguous_unit'
                $reason = 'verification intent present but command not frozen'
            } elseif ($sectionName -eq 'Phase Cleanup Contract') {
                $classification = 'advisory_only_unit'
                $reason = 'cleanup requirement declared but execution delegated to cleanup stage'
            }

            $units += [pscustomobject]@{
                unit_id = ('shadow-{0:00}' -f $unitIndex)
                source_section = $sectionName
                line = $trimmed
                classification = $classification
                reason = $reason
                extracted_commands = @($inlineCommands)
            }
        }
    }

    $shadow = [pscustomobject]@{
        generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
        run_id = $RunId
        execution_plan_path = $PlanPath
        candidate_unit_count = @($units).Count
        executable_unit_count = @($units | Where-Object { $_.classification -eq 'executable_unit' }).Count
        specialist_dispatch_unit_count = @($units | Where-Object { $_.classification -eq 'specialist_dispatch_unit' }).Count
        advisory_only_unit_count = @($units | Where-Object { $_.classification -eq 'advisory_only_unit' }).Count
        ambiguous_unit_count = @($units | Where-Object { $_.classification -eq 'ambiguous_unit' }).Count
        unsafe_unit_count = @($units | Where-Object { $_.classification -eq 'unsafe_unit' }).Count
        non_executable_narrative_count = @($units | Where-Object { $_.classification -eq 'non_executable_narrative' }).Count
        units = @($units)
        proof_class = 'structure'
        promotion_suitable = $false
    }

    $shadowPath = Join-Path $SessionRoot 'plan-derived-execution-shadow.json'
    Write-VibeJsonArtifact -Path $shadowPath -Value $shadow

    return [pscustomobject]@{
        path = $shadowPath
        payload = $shadow
    }
}

$runtime = Get-VibeRuntimeContext -ScriptPath $PSCommandPath
if ([string]::IsNullOrWhiteSpace($RunId)) {
    $RunId = New-VibeRunId
}

$sessionRoot = Ensure-VibeSessionRoot -RepoRoot $runtime.repo_root -RunId $RunId -ArtifactRoot $ArtifactRoot
$grade = Get-VibeInternalGrade -Task $Task
$requirementPath = if (-not [string]::IsNullOrWhiteSpace($RequirementDocPath)) { $RequirementDocPath } else { Get-VibeRequirementDocPath -RepoRoot $runtime.repo_root -Task $Task -ArtifactRoot $ArtifactRoot }
$planPath = if (-not [string]::IsNullOrWhiteSpace($ExecutionPlanPath)) { $ExecutionPlanPath } else { Get-VibeExecutionPlanPath -RepoRoot $runtime.repo_root -Task $Task -ArtifactRoot $ArtifactRoot }
$runtimeInputPath = if (-not [string]::IsNullOrWhiteSpace($RuntimeInputPacketPath)) { $RuntimeInputPacketPath } else { Get-VibeRuntimeInputPacketPath -RepoRoot $runtime.repo_root -RunId $RunId -ArtifactRoot $ArtifactRoot }
$runtimeInputPacket = if (Test-Path -LiteralPath $runtimeInputPath) {
    Get-Content -LiteralPath $runtimeInputPath -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    $null
}
$hierarchyState = Get-VibeHierarchyState `
    -GovernanceScope $(if ($runtimeInputPacket) { [string]$runtimeInputPacket.governance_scope } else { $GovernanceScope }) `
    -RunId $RunId `
    -RootRunId $(if ($runtimeInputPacket -and $runtimeInputPacket.hierarchy) { [string]$runtimeInputPacket.hierarchy.root_run_id } else { $RootRunId }) `
    -ParentRunId $(if ($runtimeInputPacket -and $runtimeInputPacket.hierarchy) { [string]$runtimeInputPacket.hierarchy.parent_run_id } else { $ParentRunId }) `
    -ParentUnitId $(if ($runtimeInputPacket -and $runtimeInputPacket.hierarchy) { [string]$runtimeInputPacket.hierarchy.parent_unit_id } else { $ParentUnitId }) `
    -InheritedRequirementDocPath $(if ($runtimeInputPacket -and $runtimeInputPacket.hierarchy) { [string]$runtimeInputPacket.hierarchy.inherited_requirement_doc_path } else { $RequirementDocPath }) `
    -InheritedExecutionPlanPath $(if ($runtimeInputPacket -and $runtimeInputPacket.hierarchy) { [string]$runtimeInputPacket.hierarchy.inherited_execution_plan_path } else { $ExecutionPlanPath }) `
    -HierarchyContract $runtime.runtime_input_packet_policy.hierarchy_contract

$policy = $runtime.benchmark_execution_policy
$proofRegistry = $runtime.proof_class_registry
$profile = $null
foreach ($candidate in @($policy.profiles)) {
    if ([string]$candidate.id -eq [string]$policy.default_profile_id) {
        $profile = $candidate
        break
    }
}
if ($null -eq $profile) {
    throw 'Unable to resolve benchmark execution profile from config/benchmark-execution-policy.json.'
}

$logsRoot = Join-Path $sessionRoot 'execution-logs'
$resultsRoot = Join-Path $sessionRoot 'execution-results'
$proofRoot = Join-Path $sessionRoot ([string]$profile.proof_bundle_dirname)
New-Item -ItemType Directory -Path $logsRoot -Force | Out-Null
New-Item -ItemType Directory -Path $resultsRoot -Force | Out-Null
New-Item -ItemType Directory -Path $proofRoot -Force | Out-Null

$tokens = @{
    '${REPO_ROOT}' = [System.IO.Path]::GetFullPath($runtime.repo_root)
    '${SESSION_ROOT}' = [System.IO.Path]::GetFullPath($sessionRoot)
    '${REQUIREMENT_DOC}' = [System.IO.Path]::GetFullPath($requirementPath)
    '${EXECUTION_PLAN}' = [System.IO.Path]::GetFullPath($planPath)
    '${RUN_ID}' = [string]$RunId
    '${ROOT_RUN_ID}' = [string]$hierarchyState.root_run_id
}
$planShadow = Get-VibePlanDerivedExecutionShadow -PlanPath $planPath -RunId $RunId -SessionRoot $sessionRoot
$specialistRecommendations = if ($runtimeInputPacket) { @($runtimeInputPacket.specialist_recommendations) } else { @() }
$approvedDispatch = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { @($runtimeInputPacket.specialist_dispatch.approved_dispatch) } else { @() }
$localSuggestions = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { @($runtimeInputPacket.specialist_dispatch.local_specialist_suggestions) } else { @() }
$specialistSkills = @($approvedDispatch | ForEach-Object { [string]$_.skill_id } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
$escalationRequired = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { [bool]$runtimeInputPacket.specialist_dispatch.escalation_required } else { $false }
$escalationPath = $null
if ([string]$hierarchyState.governance_scope -eq 'child' -and $escalationRequired) {
    $escalation = [pscustomobject]@{
        run_id = $RunId
        governance_scope = [string]$hierarchyState.governance_scope
        root_run_id = [string]$hierarchyState.root_run_id
        parent_run_id = if ($null -eq $hierarchyState.parent_run_id) { $null } else { [string]$hierarchyState.parent_run_id }
        parent_unit_id = if ($null -eq $hierarchyState.parent_unit_id) { $null } else { [string]$hierarchyState.parent_unit_id }
        approval_owner = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { [string]$runtimeInputPacket.specialist_dispatch.approval_owner } else { 'root_vibe' }
        status = 'root_approval_required'
        requested_specialist_skill_ids = @($localSuggestions | ForEach-Object { [string]$_.skill_id } | Select-Object -Unique)
        local_specialist_suggestions = @($localSuggestions)
        generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    }
    $escalationPath = Join-Path $sessionRoot 'specialist-escalation-request.json'
    Write-VibeJsonArtifact -Path $escalationPath -Value $escalation
}

$waveReceipts = @()
$resultPaths = @()
$executedUnitCount = 0
$successfulUnitCount = 0
$failedUnitCount = 0
$timedOutUnitCount = 0
$plannedUnitCount = 0

foreach ($wave in @($profile.waves)) {
    $waveStartedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $waveResults = @()
    $plannedUnitCount += @($wave.units).Count

    foreach ($unit in @($wave.units)) {
        $executed = Invoke-VibeExecutionUnit -Unit $unit -RepoRoot $runtime.repo_root -SessionRoot $sessionRoot -Tokens $tokens -DefaultTimeoutSeconds ([int]$policy.scheduler.default_timeout_seconds)
        $waveResults += $executed.result
        $resultPaths += $executed.result_path
        $executedUnitCount += 1
        if ([bool]$executed.result.verification_passed) {
            $successfulUnitCount += 1
        } elseif ([bool]$executed.result.timed_out) {
            $timedOutUnitCount += 1
            $failedUnitCount += 1
        } else {
            $failedUnitCount += 1
        }
    }

    $waveReceipts += [pscustomobject]@{
        wave_id = [string]$wave.wave_id
        description = [string]$wave.description
        status = if (@($waveResults | Where-Object { -not $_.verification_passed }).Count -eq 0) { 'completed' } else { 'failed' }
        started_at = $waveStartedAt
        finished_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
        planned_unit_count = @($wave.units).Count
        executed_unit_count = @($waveResults).Count
        units = @($waveResults | ForEach-Object {
            [pscustomobject]@{
                unit_id = [string]$_.unit_id
                status = [string]$_.status
                exit_code = [int]$_.exit_code
                result_path = (Join-Path $resultsRoot ("{0}.json" -f $_.unit_id))
            }
        })
    }
}

$baseStatus = if ($failedUnitCount -eq 0 -and $executedUnitCount -ge [int]$profile.expected_minimum_units) { 'completed' } elseif ($executedUnitCount -eq 0) { 'failed' } else { 'completed_with_failures' }
$executionManifest = [pscustomobject]@{
    stage = 'plan_execute'
    run_id = $RunId
    governance_scope = [string]$hierarchyState.governance_scope
    mode = $Mode
    internal_grade = $grade
    scheduler_kind = [string]$policy.scheduler.kind
    profile_id = [string]$profile.id
    requirement_doc_path = $requirementPath
    execution_plan_path = $planPath
    runtime_input_packet_path = $runtimeInputPath
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    planned_wave_count = @($profile.waves).Count
    planned_unit_count = $plannedUnitCount
    executed_unit_count = $executedUnitCount
    successful_unit_count = $successfulUnitCount
    failed_unit_count = $failedUnitCount
    timed_out_unit_count = $timedOutUnitCount
    proof_class = [string]$proofRegistry.artifact_class_defaults.execution_manifest
    promotion_suitable = [string]$proofRegistry.promotion_suitability.runtime
    hierarchy = [pscustomobject]@{
        governance_scope = [string]$hierarchyState.governance_scope
        root_run_id = [string]$hierarchyState.root_run_id
        parent_run_id = if ($null -eq $hierarchyState.parent_run_id) { $null } else { [string]$hierarchyState.parent_run_id }
        parent_unit_id = if ($null -eq $hierarchyState.parent_unit_id) { $null } else { [string]$hierarchyState.parent_unit_id }
        inherited_requirement_doc_path = if ($null -eq $hierarchyState.inherited_requirement_doc_path) { $null } else { [string]$hierarchyState.inherited_requirement_doc_path }
        inherited_execution_plan_path = if ($null -eq $hierarchyState.inherited_execution_plan_path) { $null } else { [string]$hierarchyState.inherited_execution_plan_path }
    }
    authority = [pscustomobject]@{
        canonical_requirement_write_allowed = [bool]$hierarchyState.allow_requirement_freeze
        canonical_plan_write_allowed = [bool]$hierarchyState.allow_plan_freeze
        global_dispatch_allowed = [bool]$hierarchyState.allow_global_dispatch
        completion_claim_allowed = [bool]$hierarchyState.allow_completion_claim
    }
    route_runtime_alignment = [pscustomobject]@{
        router_selected_skill = if ($runtimeInputPacket) { [string]$runtimeInputPacket.route_snapshot.selected_skill } else { $null }
        runtime_selected_skill = if ($runtimeInputPacket) { [string]$runtimeInputPacket.authority_flags.explicit_runtime_skill } else { 'vibe' }
        skill_mismatch = if ($runtimeInputPacket) { [bool]$runtimeInputPacket.divergence_shadow.skill_mismatch } else { $false }
        confirm_required = if ($runtimeInputPacket) { [bool]$runtimeInputPacket.route_snapshot.confirm_required } else { $false }
    }
    plan_shadow = [pscustomobject]@{
        path = $planShadow.path
        candidate_unit_count = [int]$planShadow.payload.candidate_unit_count
        executable_unit_count = [int]$planShadow.payload.executable_unit_count
        specialist_dispatch_unit_count = [int]$planShadow.payload.specialist_dispatch_unit_count
        advisory_only_unit_count = [int]$planShadow.payload.advisory_only_unit_count
        ambiguous_unit_count = [int]$planShadow.payload.ambiguous_unit_count
    }
    specialist_accounting = [pscustomobject]@{
        recommendation_count = @($specialistRecommendations).Count
        specialist_skill_count = @($specialistSkills).Count
        specialist_skills = @($specialistSkills)
        native_usage_required = [bool](@($specialistRecommendations | Where-Object { $_.native_usage_required }).Count -gt 0)
        dispatch_unit_count = [int]$planShadow.payload.specialist_dispatch_unit_count
        recommendations = @($specialistRecommendations)
        approved_dispatch_count = @($approvedDispatch).Count
        approved_dispatch = @($approvedDispatch)
        local_suggestion_count = @($localSuggestions).Count
        local_specialist_suggestions = @($localSuggestions)
        escalation_required = [bool]$escalationRequired
        escalation_request_path = $escalationPath
    }
    status = if ([string]$hierarchyState.governance_scope -eq 'child' -and $baseStatus -eq 'completed') { 'completed_local_scope' } else { $baseStatus }
    waves = @($waveReceipts)
}

$executionManifestPath = Join-Path $sessionRoot 'execution-manifest.json'
Write-VibeJsonArtifact -Path $executionManifestPath -Value $executionManifest

$proofManifest = [pscustomobject]@{
    bundle_kind = 'benchmark_autonomous_execution_proof'
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    run_id = $RunId
    mode = $Mode
    task = $Task
    session_root = $sessionRoot
    execution_manifest_path = $executionManifestPath
    plan_shadow_path = $planShadow.path
    result_paths = @($resultPaths)
    executed_unit_count = $executedUnitCount
    successful_unit_count = $successfulUnitCount
    failed_unit_count = $failedUnitCount
    minimum_units_required = [int]$profile.expected_minimum_units
    proof_class = [string]$proofRegistry.artifact_class_defaults.benchmark_proof_manifest
    promotion_suitable = [string]$proofRegistry.promotion_suitability.runtime
    specialist_recommendation_count = @($specialistRecommendations).Count
    specialist_dispatch_unit_count = [int]$planShadow.payload.specialist_dispatch_unit_count
    governance_scope = [string]$hierarchyState.governance_scope
    escalation_required = [bool]$escalationRequired
    proof_passed = [bool](($failedUnitCount -eq 0) -and ($executedUnitCount -ge [int]$profile.expected_minimum_units))
}
$proofManifestPath = Join-Path $proofRoot 'manifest.json'
Write-VibeJsonArtifact -Path $proofManifestPath -Value $proofManifest

$proofLines = @(
    '# Benchmark Autonomous Proof',
    '',
    ('- run_id: `{0}`' -f $RunId),
    ('- mode: `{0}`' -f $Mode),
    ('- profile: `{0}`' -f ([string]$profile.id)),
    ('- proof_class: `{0}`' -f ([string]$proofManifest.proof_class)),
    ('- executed_unit_count: `{0}`' -f $executedUnitCount),
    ('- successful_unit_count: `{0}`' -f $successfulUnitCount),
    ('- failed_unit_count: `{0}`' -f $failedUnitCount),
    ('- specialist_recommendation_count: `{0}`' -f @($specialistRecommendations).Count),
    ('- specialist_dispatch_unit_count: `{0}`' -f [int]$planShadow.payload.specialist_dispatch_unit_count),
    ('- execution_manifest: `{0}`' -f $executionManifestPath),
    ('- plan_shadow: `{0}`' -f $planShadow.path),
    ''
)
foreach ($waveReceipt in @($waveReceipts)) {
    $proofLines += @(
        "## $([string]$waveReceipt.wave_id)",
        "- status: $([string]$waveReceipt.status)",
        "- executed_unit_count: $([int]$waveReceipt.executed_unit_count)"
    )
    foreach ($unitReceipt in @($waveReceipt.units)) {
        $proofLines += ('- unit `{0}` -> status `{1}`, exit_code `{2}`' -f ([string]$unitReceipt.unit_id), ([string]$unitReceipt.status), ([int]$unitReceipt.exit_code))
    }
    $proofLines += ''
}
$proofSummaryPath = Join-Path $proofRoot 'operation-record.md'
Write-VibeMarkdownArtifact -Path $proofSummaryPath -Lines $proofLines

$receipt = [pscustomobject]@{
    stage = 'plan_execute'
    run_id = $RunId
    governance_scope = [string]$hierarchyState.governance_scope
    mode = $Mode
    internal_grade = $grade
    status = [string]$executionManifest.status
    requirement_doc_path = $requirementPath
    execution_plan_path = $planPath
    runtime_input_packet_path = $runtimeInputPath
    plan_shadow_path = $planShadow.path
    execution_manifest_path = $executionManifestPath
    benchmark_proof_manifest_path = $proofManifestPath
    executed_unit_count = $executedUnitCount
    successful_unit_count = $successfulUnitCount
    failed_unit_count = $failedUnitCount
    specialist_recommendation_count = @($specialistRecommendations).Count
    specialist_dispatch_unit_count = [int]$planShadow.payload.specialist_dispatch_unit_count
    specialist_skills = @($specialistSkills)
    local_specialist_suggestion_count = @($localSuggestions).Count
    escalation_required = [bool]$escalationRequired
    escalation_request_path = $escalationPath
    completion_claim_allowed = [bool]$hierarchyState.allow_completion_claim
    proof_class = [string]$proofRegistry.artifact_class_defaults.execution_manifest
    verification_contract = @(
        'No completion claim without verification evidence.',
        'All subagent prompts must end with $vibe.',
        'Specialist help must preserve native workflow and remain bounded under vibe governance.',
        'Child-governed lanes may not issue final completion claims or mutate canonical requirement/plan truth.',
        'Phase cleanup must run after execution.'
    )
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
}

$receiptPath = Join-Path $sessionRoot 'phase-execute.json'
Write-VibeJsonArtifact -Path $receiptPath -Value $receipt

[pscustomobject]@{
    run_id = $RunId
    session_root = $sessionRoot
    receipt_path = $receiptPath
    plan_shadow_path = $planShadow.path
    execution_manifest_path = $executionManifestPath
    benchmark_proof_manifest_path = $proofManifestPath
    receipt = $receipt
}
