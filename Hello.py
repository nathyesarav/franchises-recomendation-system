# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
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

import streamlit as st
from streamlit.logger import get_logger
from PIL import Image

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Sistema de Recomendación",
        page_icon="📊",
    )

    st.write("# Sistema de Recomendación")



    st.markdown(
        """
        El Sistema de Recomendación tiene los siguientes módulos que se pueden seleccionar en el menù a la izquierda:
        - Recomendación de Franquicias parecidas a la franquicia seleccionada
        - Recomendación de Franquicias para un usuario seleccionado
        - Recomendación de ciudades para invertir
        - Categorías conmayor y menor expectativa de Crecimiento
    """
    )


if __name__ == "__main__":
    run()
