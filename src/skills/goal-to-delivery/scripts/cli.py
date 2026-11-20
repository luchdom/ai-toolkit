"""Thin executable wrapper over the canonical local-work package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts.errors import DeliveryBaseError, ValidationError
    from scripts.redaction import redact_value
    from scripts.workflow_init import WorkflowManager
else:
    from .errors import DeliveryBaseError, ValidationError
    from .redaction import redact_value
    from .workflow_init import WorkflowManager


def _manager(arguments: argparse.Namespace, *, root_name: str = "repository_root") -> WorkflowManager:
    return WorkflowManager(
        getattr(arguments, root_name),
        repository_key=arguments.repository_key,
        state_home_override=arguments.state_home,
    )


def _verify_assignment(arguments: argparse.Namespace) -> dict[str, str]:
    """Check the registration bound to a coordinator's already verified assignment."""
    manager = WorkflowManager(
        arguments.repository_root,
        repository_key=arguments.repository_key,
        state_home_override=arguments.state_home,
        prepare_state=False,
    )
    if Path(manager.identity.git_dir) == Path(manager.identity.common_dir):
        raise ValidationError("The assigned repository must be a linked issue worktree")
    descriptor = manager.inspect_registration(workflow_id=arguments.workflow_id)
    if Path(arguments.repository_root) != Path(descriptor["repositoryRoot"]):
        raise ValidationError("The assigned worktree differs from the registered repository root")
    if Path(arguments.artifact_folder) != Path(descriptor["artifactFolder"]):
        raise ValidationError("The assigned artifact folder differs from the registered folder")
    if arguments.completion_boundary != descriptor["completionBoundary"]:
        raise ValidationError("The assigned completion boundary differs from the registered boundary")

    if arguments.local_work_key is None:
        if descriptor["tracking"] != {"provider": "linear", "externalId": arguments.issue_id}:
            raise ValidationError("The assigned issue differs from the registered Linear issue")
    else:
        # The trusted fixture board owns the issueId-to-workKey mapping.
        if descriptor["workSource"] != "local" or descriptor["tracking"]["provider"] != "none":
            raise ValidationError("A local fixture mapping requires an untracked local registration")
        if not arguments.issue_id.strip() or arguments.local_work_key != descriptor["workKey"]:
            raise ValidationError("The local fixture needs an issue ID and its registered work key")
        if arguments.completion_boundary not in {"artifact", "working-tree"}:
            raise ValidationError("A local fixture mapping supports only local completion boundaries")

    return {"status": "verified", "workflowId": descriptor["workflowId"]}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="workflow-init")
    subcommands = parser.add_subparsers(dest="command", required=True)
    boundaries = ("artifact", "working-tree", "commit", "pr", "merge")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repository-root", required=True)
    common.add_argument("--repository-key", required=True)
    common.add_argument("--state-home")

    initialize = subcommands.add_parser("init", parents=[common])
    initialize.add_argument("--workflow", choices=("manual", "semi-autonomous"), required=True)
    initialize.add_argument("--goal", required=True)
    initialize.add_argument("--display-title")
    initialize.add_argument(
        "--completion-boundary",
        choices=boundaries,
        default="working-tree",
    )

    resume = subcommands.add_parser("resume", parents=[common])
    selectors = resume.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--workflow-id")
    selectors.add_argument("--artifact-path")
    selectors.add_argument("--external-id")

    verify = subcommands.add_parser("verify-assignment", parents=[common])
    verify.add_argument("--workflow-id", required=True)
    verify.add_argument("--artifact-folder", required=True)
    verify.add_argument("--issue-id", required=True)
    verify.add_argument("--completion-boundary", required=True, choices=boundaries)
    verify.add_argument("--local-work-key", help="Exact registered work key for a local fixture board")

    attach = subcommands.add_parser("attach", parents=[common])
    attach.add_argument("--workflow-id", required=True)
    attach.add_argument("--provider", choices=("linear",), required=True)
    attach.add_argument("--external-id", required=True)

    handoff = subcommands.add_parser("handoff")
    handoff.add_argument("--source-root", required=True)
    handoff.add_argument("--destination-root", required=True)
    handoff.add_argument("--repository-key", required=True)
    handoff.add_argument("--state-home")
    handoff.add_argument("--workflow-id", required=True)
    handoff.add_argument(
        "--expected-path",
        action="append",
        dest="expected_paths",
        required=True,
        help="Exact canonical repo-relative Git-changed path; repeat for each intended path",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "init":
            result = _manager(arguments).initialize_local(
                workflow=arguments.workflow,
                goal=arguments.goal,
                display_title=arguments.display_title,
                completion_boundary=arguments.completion_boundary,
            )
        elif arguments.command == "resume":
            result = _manager(arguments).resume(
                workflow_id=arguments.workflow_id,
                artifact_path=arguments.artifact_path,
                external_id=arguments.external_id,
            )
        elif arguments.command == "attach":
            result = _manager(arguments).attach_linear(
                workflow_id=arguments.workflow_id,
                external_id=arguments.external_id,
            )
        elif arguments.command == "verify-assignment":
            result = _verify_assignment(arguments)
        else:
            result = WorkflowManager(
                arguments.source_root,
                repository_key=arguments.repository_key,
                state_home_override=arguments.state_home,
            ).workflow_managed_handoff(
                workflow_id=arguments.workflow_id,
                destination_root=arguments.destination_root,
                expected_paths=arguments.expected_paths,
            )
        print(json.dumps(redact_value(result), sort_keys=True))
        return 0
    except DeliveryBaseError as exc:
        print(json.dumps({"status": "failed", "error": redact_value(str(exc))}), file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as exc:
        # Expected machine-environment failures only; programmer defects still surface.
        print(
            json.dumps(
                {
                    "status": "failed",
                    "error": f"Expected environment I/O failure ({type(exc).__name__})",
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
