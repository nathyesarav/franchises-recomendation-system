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

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Sistema de Recomendación",
        page_icon="📊",
    )

    st.write("# Sistema de Recomendación")

    st.markdown(
        """
        El Sistema de Recomendación tiene los siguientes módulos:
        - [Recomendación de Franquicias parecidas a la franquicia seleccionada](https://franchisesrecomendationsystem-27pot0lzc4n.streamlit.app/Recommendation_System_Franquicias)
        - [Recomendación de Franquicias para un usuario seleccionado]
        (https://franchisesrecomendationsystem-27pot0lzc4n.streamlit.app/Recommendation_System_Usuarios)
        - [Recomendación de ciudades para invertir]
        (https://franchisesrecomendationsystem-27pot0lzc4n.streamlit.app/Ciudades_Para_Invertir)
        - [Categorías conmayor y menor expectativa de Crecimiento]
        (https://github.com/streamlit/Expectativas_De_Crecimiento)
    """
    )


if __name__ == "__main__":
    run()
