from __future__ import annotations

import dataclasses
import logging
from pathlib import Path
from typing import Type

from dbt.adapters.base.impl import BaseAdapter
from dbt.adapters.factory import get_adapter_by_type
from dbt.cli.main import dbtRunner
from dbt.config.profile import Profile
from dbt.config.project import Project
from dbt.config.runtime import load_profile, load_project
from dbt_semantic_interfaces.implementations.semantic_manifest import PydanticSemanticManifest
from dbt_semantic_interfaces.pretty_print import pformat_big_objects
from dbt_semantic_interfaces.protocols.semantic_manifest import SemanticManifest
from dbt_semantic_interfaces.transformations.semantic_manifest_transformer import PydanticSemanticManifestTransformer
from typing_extensions import Self

from metricflow.errors.errors import ModelCreationException

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class dbtArtifacts:
    """Container with access to the dbt artifacts required to power the MetricFlow CLI."""

    profile: Profile
    project: Project
    adapter: BaseAdapter
    semantic_manifest: SemanticManifest

    @classmethod
    def load_from_project_path(cls: Type[Self], project_path: Path) -> Self:
        """Loads all dbt artifacts for the project associated with the given project path."""
        logger.info(f"Loading dbt artifacts for project located at {project_path}")
        dbtRunner().invoke(["-q", "debug"], project_dir=str(project_path))
        profile = load_profile(str(project_path), {})
        project = load_project(str(project_path), version_check=False, profile=profile)
        logger.info(f"Loaded project {project.project_name} with profile details:\n{pformat_big_objects(profile)}")
        # dbt's get_adapter helper expects an AdapterRequiredConfig, but `project` is missing cli_vars
        # In practice, get_adapter only actually requires HasCredentials, so we replicate the type extraction
        # from get_adapter here rather than spinning up a full RuntimeConfig instance
        # TODO: Move to a fully supported interface when one becomes available
        adapter = get_adapter_by_type(profile.credentials.type)
        semantic_manifest = dbtArtifacts.build_semantic_manifest_from_dbt_project_root(project_root=project_path)
        return cls(profile=profile, project=project, adapter=adapter, semantic_manifest=semantic_manifest)

    @staticmethod
    def build_semantic_manifest_from_dbt_project_root(project_root: Path) -> SemanticManifest:
        """In the dbt project root, retrieve the manifest path and parse the SemanticManifest."""
        DEFAULT_TARGET_PATH = "target/semantic_manifest.json"
        full_path_to_manifest = Path(project_root, DEFAULT_TARGET_PATH).resolve()
        if not full_path_to_manifest.exists():
            raise ModelCreationException(
                f"Unable to find {full_path_to_manifest}\n"
                "Please ensure that you are running `mf` in the root directory of a dbt project "
                "and that the semantic_manifest JSON exists."
            )
        try:
            with open(full_path_to_manifest, "r") as file:
                raw_contents = file.read()
                raw_model = PydanticSemanticManifest.parse_raw(raw_contents)
                # The serialized object in the dbt project does not have all transformations applied to it at
                # this time, which causes failures with input measure resolution.
                # TODO: remove this transform call once the upstream changes are integrated into our dependency tree
                model = PydanticSemanticManifestTransformer.transform(raw_model)
                return model
        except Exception as e:
            raise ModelCreationException from e
