"""
HOW TO DEPLOY TO STREAMLIT CLOUD:

1. Go to streamlit.io
2. Sign in with GitHub
3. Connect your repository
4. Add these files:
   - requirements.txt
      - lowpoly_generator.py (rename to app.py for auto-detection)
         - .streamlit/secrets.toml (for API keys)

         5. In secrets.toml add:
            GEMINI_API_KEY = "your-key-here"

            6. Streamlit will auto-deploy!

            For mobile testing:
            - Open phone browser
            - Go to your-app-name.streamlit.app
            - Add to home screen (works like native app)
            """

            # Минимальная версия для быстрого старта
            import streamlit as st
            import numpy as np

            st.title("🚀 3D Model Generator")
            st.write("Quick start template for mobile")

            # Простой генератор без зависимостей
            if st.button("Generate Simple Model"):
                st.success("Model generated!")
                    st.code("""
                        // In production version:
                            // - Add trimesh for 3D
                                // - Add plotly for visualization
                                    // - Add export functionality
                                        """)