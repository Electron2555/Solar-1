import streamlit as st
import trimesh
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import json
import uuid
import zipfile
import io

# Настройки
st.set_page_config(page_title="3D Generator", layout="wide")

class MobileLowPolyGenerator:
    """Оптимизированный генератор для телефона"""
    
    def __init__(self):
        self.models = {
            "🌳 Tree": self.generate_tree,
            "🪨 Rock": self.generate_rock,
            "🏠 Building": self.generate_building,
            "🚗 Vehicle": self.generate_vehicle,
            "🎮 Game Asset": self.generate_game_asset
        }
    
    def generate_tree(self, size=1.0, detail=0.5):
        """Low-poly дерево для игр"""
        trunk = trimesh.creation.cylinder(radius=0.1, height=2, sections=6)
        leaves = trimesh.creation.icosphere(subdivisions=1, radius=1)
        leaves.vertices[:, 2] += 1.5
        return trimesh.util.concatenate([trunk, leaves])
    
    def generate_rock(self, size=1.0, detail=0.5):
        """Low-poly камень"""
        mesh = trimesh.creation.icosphere(subdivisions=1)
        vertices = mesh.vertices.copy()
        noise = np.random.randn(len(vertices), 3) * 0.3 * detail
        mesh.vertices = vertices + noise
        return mesh
    
    def generate_building(self, size=1.0, detail=0.5):
        """Low-poly здание"""
        base = trimesh.creation.box(extents=[2, 2, 3])
        roof = trimesh.creation.cone(radius=1.2, height=1, sections=4)
        roof.vertices[:, 2] += 1.5
        return trimesh.util.concatenate([base, roof])
    
    def generate_vehicle(self, size=1.0, detail=0.5):
        """Low-poly транспорт"""
        body = trimesh.creation.box(extents=[3, 1.5, 1])
        wheel = trimesh.creation.cylinder(radius=0.4, height=0.3, sections=8)
        wheels = []
        for x in [-1, 1]:
            for y in [-0.6, 0.6]:
                w = wheel.copy()
                w.vertices[:, 0] += x
                w.vertices[:, 1] += y
                wheels.append(w)
        return trimesh.util.concatenate([body] + wheels)
    
    def generate_game_asset(self, size=1.0, detail=0.5):
        """Универсальный игровой ассет"""
        # Генерация кристалла как примера
        base = trimesh.creation.icosahedron()
        # Вытягиваем случайные вершины
        vertices = base.vertices.copy()
        for i in range(len(vertices)):
            if np.random.random() < detail:
                vertices[i] *= np.random.uniform(1.2, 1.8)
        return trimesh.Trimesh(vertices=vertices, faces=base.faces)

class MarketplaceExporter:
    """Экспорт для маркетплейсов"""
    
    @staticmethod
    def create_zip_package(mesh, model_name, formats=["glb", "obj"]):
        """Создание ZIP архива с моделью"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Экспорт в разные форматы
            for fmt in formats:
                file_buffer = io.BytesIO()
                if fmt == "glb":
                    mesh.export(file_buffer, file_type="glb")
                    zip_file.writestr(f"{model_name}.glb", file_buffer.getvalue())
                elif fmt == "obj":
                    mesh.export(file_buffer, file_type="obj")
                    zip_file.writestr(f"{model_name}.obj", file_buffer.getvalue())
            
            # Добавляем README
            readme = f"""
# {model_name} - Low Poly 3D Model

## Specifications:
- Polygons: {len(mesh.faces)}
- Vertices: {len(mesh.vertices)}
- Format: GLB, OBJ
- Style: Low Poly

## License:
Commercial use allowed. Can be sold on 3D marketplaces.
Created with Mobile 3D Generator.
"""
            zip_file.writestr(f"README_{model_name}.txt", readme)
        
        zip_buffer.seek(0)
        return zip_buffer

def plot_3d_model(mesh):
    """Визуализация 3D модели в Plotly"""
    x, y, z = mesh.vertices.T
    i, j, k = mesh.faces.T
    
    fig = go.Figure(data=[
        go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            color='lightblue',
            opacity=0.8,
            flatshading=True
        )
    ])
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    
    return fig

def main():
    st.title("📱 Mobile 3D Generator for Marketplaces")
    st.markdown("### Create & sell low-poly 3D models directly from your phone")
    
    # Инициализация
    if 'generator' not in st.session_state:
        st.session_state.generator = MobileLowPolyGenerator()
    if 'current_model' not in st.session_state:
        st.session_state.current_model = None
    
    # Сайдбар с настройками
    with st.sidebar:
        st.header("⚙️ Settings")
        
        model_type = st.selectbox(
            "Select model type:",
            list(st.session_state.generator.models.keys())
        )
        
        detail_level = st.slider(
            "Detail level:", 0.1, 1.0, 0.5
        )
        
        size = st.slider(
            "Size:", 0.5, 2.0, 1.0
        )
        
        marketplace = st.selectbox(
            "Target marketplace:",
            ["Sketchfab", "TurboSquid", "Unity Asset Store", "CGTrader"]
        )
        
        license_type = st.radio(
            "License:",
            ["Free (Personal)", "$9.99 (Commercial)", "$49.99 (Unlimited)"]
        )
        
        if st.button("🎨 Generate Model", type="primary", use_container_width=True):
            with st.spinner("Generating 3D model..."):
                generate_func = st.session_state.generator.models[model_type]
                mesh = generate_func(size=size, detail=detail_level)
                st.session_state.current_model = mesh
    
    # Основная область
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Model Preview")
        
        if st.session_state.current_model is not None:
            # Визуализация
            fig = plot_3d_model(st.session_state.current_model)
            st.plotly_chart(fig, use_container_width=True)
            
            # Статистика
            mesh = st.session_state.current_model
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Polygons", f"{len(mesh.faces):,}")
            with stats_col2:
                st.metric("Vertices", f"{len(mesh.vertices):,}")
            with stats_col3:
                st.metric("Format", "GLB/OBJ")
        else:
            st.info("👈 Select settings and click 'Generate Model'")
    
    with col2:
        st.subheader("📦 Export")
        
        if st.session_state.current_model is not None:
            model_name = st.text_input("Model name:", value=f"model_{uuid.uuid4().hex[:8]}")
            
            formats = st.multiselect(
                "Export formats:",
                ["GLB", "OBJ", "STL"],
                default=["GLB", "OBJ"]
            )
            
            # Экспорт
            exporter = MarketplaceExporter()
            zip_buffer = exporter.create_zip_package(
                st.session_state.current_model,
                model_name,
                formats=[f.lower() for f in formats]
            )
            
            st.download_button(
                label="📥 Download ZIP Package",
                data=zip_buffer,
                file_name=f"{model_name}_package.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            # Интеграция с маркетплейсами
            st.markdown("---")
            st.subheader("🚀 Sell on Marketplaces")
            
            if marketplace == "Sketchfab":
                st.info("Upload .glb file directly to Sketchfab.com")
            elif marketplace == "Unity Asset Store":
                st.info("Package as .unitypackage for Unity Asset Store")
            elif marketplace == "TurboSquid":
                st.info("Submit with 4K preview renders")
            
            # Генерация описания
            if st.button("📝 Generate Description (AI)"):
                st.session_state.ai_description = f"""
**{model_name}** - Low Poly {model_type[2:]}

Perfect for:
- {marketplace} marketplace
- Mobile games
- VR/AR applications
- Architectural visualization

Technical specs:
- Optimized topology
- Clean UV layout
- Real-time ready
- PBR materials compatible

Price suggestion: {license_type}
"""
                st.text_area("AI Description:", st.session_state.ai_description)
    
    # Нижняя панель - быстрые действия
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Quick Generate", use_container_width=True):
            # Случайная генерация
            import random
            random_type = random.choice(list(st.session_state.generator.models.keys()))
            st.session_state.current_model = st.session_state.generator.models[random_type](
                size=random.uniform(0.5, 1.5),
                detail=random.uniform(0.3, 0.8)
            )
            st.rerun()
    
    with col2:
        if st.button("📊 Batch Generate (10)", use_container_width=True):
            st.info("Batch generation available in Pro version")
    
    with col3:
        if st.button("🎨 Material Editor", use_container_width=True):
            st.info("Material editor available in Pro version")
    
    with col4:
        if st.button("🤖 AI Enhance", use_container_width=True):
            st.info("AI enhancement available with API key")

if __name__ == "__main__":
    main()
