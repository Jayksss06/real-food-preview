"""
REAL FOOD PREVIEW — Blender 3D & Model Context Protocol (MCP) Automation Script
Program Studi Teknologi Rekayasa Multimedia - Politeknik Negeri Media Kreatif (2026)
Disusun oleh: Rakha Danendra (2490343132) & Satria Ilham (2490343144)

Fungsi:
1. Membuat objek 3D Piring Keramik Nusantara & Hidangan 3D Utuh (3D Main Dish).
2. Membuat objek 3D Struk Kertas Komposisi (Floating Paper Receipt) berbasis Plane Mesh
   di samping piring dengan material kertas matte (Roughness = 0.92, Specular rendah) agar tidak silau.
3. Menempelkan tekstur gambar daftar ingredients (.png) ke permukaan mesh struk kertas.
4. Mengekspor satu kesatuan objek 3D ke dalam format .glb (WebAR) dan .fbx (Unity/Vuforia).
"""

import os
import math
import bpy


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def create_pbr_material(name, base_color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def create_matte_receipt_material(name, texture_path):
    """
    Membuat material Struk Kertas Kasir (Floating Paper Receipt) dengan
    pengaturan Roughness tinggi (0.92) agar menyerupai kertas doff/matte dan tidak silau.
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    bsdf.inputs["Roughness"].default_value = 0.92
    bsdf.inputs["Metallic"].default_value = 0.0

    if os.path.exists(texture_path):
        tex_image = nodes.new("ShaderNodeTexImage")
        tex_image.image = bpy.data.images.load(texture_path)
        links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.96, 0.94, 0.90, 1.0)

    return mat


def build_nasi_bakar_roa_scene(receipt_texture_path, export_dir):
    clear_scene()

    # 1. Piring Keramik Coklat Remboelan
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.15, depth=0.12, location=(-0.75, 0.0, 0.06))
    plate = bpy.context.active_object
    plate.name = "Piring_Remboelan"
    mat_plate = create_pbr_material("Mat_Piring_Keramik", (0.27, 0.19, 0.15, 1.0), roughness=0.28)
    plate.data.materials.append(mat_plate)

    # 2. Bungkusan Daun Pisang Bakar (Nasi Bakar Roa)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.42, depth=1.55, location=(-0.75, 0.0, 0.28),
                                        rotation=(0.0, math.radians(90), math.radians(15)))
    banana_leaf = bpy.context.active_object
    banana_leaf.name = "Daun_Pisang_Bakar"
    banana_leaf.scale = (0.65, 1.0, 1.0)
    mat_leaf = create_pbr_material("Mat_Daun_Pisang", (0.18, 0.34, 0.14, 1.0), roughness=0.55)
    banana_leaf.data.materials.append(mat_leaf)

    # 3. Isian Nasi Gurih Serai & Suwiran Ikan Roa Asap
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.38, location=(-0.75, 0.0, 0.42))
    rice_mound = bpy.context.active_object
    rice_mound.name = "Nasi_Rempah_Serai"
    rice_mound.scale = (1.65, 0.72, 0.45)
    mat_rice = create_pbr_material("Mat_Nasi_Gurih", (0.95, 0.92, 0.82, 1.0), roughness=0.78)
    rice_mound.data.materials.append(mat_rice)

    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.28, location=(-0.75, 0.0, 0.54))
    roa_topping = bpy.context.active_object
    roa_topping.name = "Suwiran_Ikan_Roa_Pedas"
    roa_topping.scale = (1.45, 0.55, 0.28)
    mat_roa = create_pbr_material("Mat_Sambal_Roa", (0.52, 0.16, 0.08, 1.0), roughness=0.62)
    roa_topping.data.materials.append(mat_roa)

    # 4. Struk Kertas Komposisi 3D (Floating Paper Receipt - Plane Mesh)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(1.05, 0.0, 0.32),
                                     rotation=(math.radians(18), 0.0, math.radians(-6)))
    receipt_mesh = bpy.context.active_object
    receipt_mesh.name = "Floating_Paper_Receipt"
    receipt_mesh.scale = (1.12, 1.68, 1.0)
    mat_receipt = create_matte_receipt_material("Mat_Struk_Komposisi_Matte", receipt_texture_path)
    receipt_mesh.data.materials.append(mat_receipt)

    # 5. Ekspor ke .glb (WebAR) dan .fbx (Unity/Vuforia)
    os.makedirs(export_dir, exist_ok=True)
    glb_path = os.path.join(export_dir, "nasi_bakar_roa_ar.glb")
    fbx_path = os.path.join(export_dir, "nasi_bakar_roa_ar.fbx")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')
    bpy.ops.export_scene.fbx(filepath=fbx_path, path_mode='COPY', embed_textures=True)
    print("Exported 3D AR Menu Asset:", glb_path, fbx_path)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tex_path = os.path.join(base_dir, "assets", "receipts", "struk_nasi_bakar_roa.png")
    out_dir = os.path.join(base_dir, "assets", "models")
    build_nasi_bakar_roa_scene(tex_path, out_dir)
