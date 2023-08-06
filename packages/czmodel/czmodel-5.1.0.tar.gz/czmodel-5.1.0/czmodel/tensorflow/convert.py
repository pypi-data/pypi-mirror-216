# CZModel provides simple-to-use conversion tools to generate a CZANN to be used in ZEISS ZEN Intellesis Portfolio
# Copyright 2022 Carl Zeiss Microscopy GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# To obtain a commercial version please contact Carl Zeiss Microscopy GmbH.
"""Provides conversion functions to generate a CZANN from exported TensorFlow models."""
import os
import sys
from typing import (
    Type,
    Tuple,
    Union,
    Sequence,
    Optional,
    TYPE_CHECKING,
    Callable,
    Generic,
    TypeVar,
)
from pathlib import Path
from tensorflow.keras.models import load_model, Model

from czmodel.core.convert import UnpackModel, parse_args
from czmodel.core.model_metadata import ModelMetadata
from czmodel.tensorflow.model_spec import ModelSpec as TensorflowModelSpec
from czmodel.core.legacy_model_metadata import ModelMetadata as LegacyModelMetadata
from czmodel.tensorflow.legacy_model_spec import ModelSpec as LegacyModelSpec

from czmodel.tensorflow.util import keras_export
from czmodel.core.util._extract_model import extract_czann_model, extract_czseg_model

if TYPE_CHECKING:
    from tensorflow.keras.layers import Layer


T = TypeVar("T", TensorflowModelSpec, LegacyModelSpec)
S = TypeVar("S", ModelMetadata, LegacyModelMetadata)


class TensorflowBaseConverter(Generic[T, S]):
    """Base class for converting models to an export format supported by the czmodel library."""

    def __init__(
        self,
        spec_type: Type[T],
        conversion_fn: Callable[
            [
                Model,
                S,
                str,
                Optional[str],
                Optional[Tuple[int, int]],
                Union["Layer", Sequence["Layer"]],
                Union["Layer", Sequence["Layer"]],
            ],
            None,
        ],
    ):
        """Initializes the converter.

        Arguments:
            spec_type: The type of the specification object.
            conversion_fn: A function to convert a model, its model specification, an output path,
                a license file, target spatial dimensions, and one or more pre- and post-processing layers
                to the target format.
        """
        self._spec_type: Type[T] = spec_type
        self.conversion_fn: Callable[
            [
                Model,
                S,
                str,
                Optional[str],
                Optional[Tuple[int, int]],
                Union["Layer", Sequence["Layer"]],
                Union["Layer", Sequence["Layer"]],
            ],
            None,
        ] = conversion_fn

    def convert_from_model_spec(
        self,
        model_spec: T,
        output_path: str,
        output_name: str = "DNNModel",
        spatial_dims: Optional[Tuple[int, int]] = None,
        preprocessing: Union["Layer", Sequence["Layer"]] = None,
        postprocessing: Union["Layer", Sequence["Layer"]] = None,
    ) -> None:
        """Convert a TensorFlow Keras model to a czann model usable in ZEN Intellesis.

        Args:
            model_spec: A ModelSpec object describing the specification of the CZANN to be generated.
            output_path: A folder to store the generated CZANN file.
            output_name: The name of the generated .czann file.
            spatial_dims: New spatial dimensions for the input node (see final usage for more details)
            preprocessing: A sequence of layers to be prepended to the model. (see final usage for more details)
            postprocessing: A sequence of layers to be appended to the model. (see final usage for more details)
        """
        # Create output directory
        os.makedirs(output_path, exist_ok=True)

        # Load model if necessary
        model = model_spec.model if isinstance(model_spec.model, Model) else load_model(model_spec.model)

        # Convert model
        self.conversion_fn(
            model,
            model_spec.model_metadata,  # type: ignore # Invalid combination must be taken care of manually
            os.path.join(output_path, output_name),
            model_spec.license_file,
            spatial_dims,
            preprocessing,
            postprocessing,
        )

    def convert_from_json_spec(
        self,
        model_spec_path: str,
        output_path: str,
        output_name: str = "DNNModel",
        spatial_dims: Optional[Tuple[int, int]] = None,
        preprocessing: Union["Layer", Sequence["Layer"]] = None,
        postprocessing: Union["Layer", Sequence["Layer"]] = None,
    ) -> None:
        """Converts a TensorFlow Keras model specified in a JSON metadata file to a czann model.

        Args:
            model_spec_path: The path to the JSON specification file.
            output_path: A folder to store the generated CZANN file.
            output_name: The name of the generated .czann file.
            spatial_dims: New spatial dimensions for the input node (see final usage for more details)
            preprocessing: A sequence of layers to be prepended to the model. (see final usage for more details)
            postprocessing: A sequence of layers to be appended to the model. (see final usage for more details)
        """
        # Parse the specification JSON file
        parsed_spec = self._spec_type.from_json(model_spec_path)

        # Write czann model to disk
        self.convert_from_model_spec(
            parsed_spec,  # type: ignore
            output_path,
            output_name,
            spatial_dims=spatial_dims,
            preprocessing=preprocessing,
            postprocessing=postprocessing,
        )


class DefaultConverter(TensorflowBaseConverter[TensorflowModelSpec, ModelMetadata], UnpackModel[ModelMetadata]):
    """Converter for czann models."""

    def __init__(self) -> None:
        """Initializes the converter for czann models."""
        super().__init__(
            spec_type=TensorflowModelSpec,
            conversion_fn=keras_export.DefaultKerasConverter().convert,
        )

    def unpack_model(
        self,
        model_file: str,
        target_dir: Path,
    ) -> Tuple[ModelMetadata, os.PathLike]:
        """Unpack the .czann file.

        Args:
            model_file: Path of the .czann file
            target_dir: Target directory for the extraction

        Returns:
            Tuple containing the model metadata and the model itself in that order
        """
        model_metadata, model_path = extract_czann_model(model_file, target_dir)
        return model_metadata, model_path


class LegacyConverter(TensorflowBaseConverter[LegacyModelSpec, LegacyModelMetadata], UnpackModel[LegacyModelMetadata]):
    """Converter for legacy czmodel models."""

    def __init__(self) -> None:
        """Initializes the converter for legacy czmodel models."""
        super().__init__(
            spec_type=LegacyModelSpec,
            conversion_fn=keras_export.LegacyKerasConverter().convert,
        )

    def unpack_model(
        self,
        model_file: str,
        target_dir: Path,
    ) -> Tuple[LegacyModelMetadata, os.PathLike]:
        """Unpack .czseg or .czmodel file.

        Args:
            model_file: Path of the .czseg/.czmodel file
            target_dir: Target directory for the extraction

        Returns:
            Tuple containing the model metadata and the model itself in that order
        """
        model_metadata, model_path = extract_czseg_model(model_file, target_dir)
        return model_metadata, model_path


def main() -> None:
    """Console script to convert a TensorFlow Keras model to a CZANN."""
    args = parse_args(sys.argv[1:])

    # Run conversion
    DefaultConverter().convert_from_json_spec(args.model_spec, args.output_path, args.output_name)


if __name__ == "__main__":
    main()
