# -*- coding: utf-8 -*-
"""Stable Diffusion v1.5 WebUI 演示界面，不加载实际模型。"""
from __future__ import annotations

import gradio as gr
import os

def load_model_click():
    return "模型状态：已就绪（演示模式，未加载真实权重）\n模型路径：stable-diffusion-v1-5\n模型类型：Stable Diffusion v1.5\n分辨率：512x512"

def generate_image(prompt: str, negative_prompt: str, num_steps: int, guidance_scale: float, seed: str):
    if not (prompt or "").strip():
        return None, "请输入提示词（prompt）。"
    
    try:
        seed_int = int(seed) if seed and seed.strip() and seed.strip() != "-1" else -1
    except:
        seed_int = -1
    
    # 演示模式：返回占位信息
    info = f"""生成参数：
- 提示词：{prompt}
- 负面提示词：{negative_prompt or '无'}
- 采样步数：{num_steps}
- 引导强度：{guidance_scale}
- 随机种子：{seed_int if seed_int != -1 else '随机'}

[演示模式] 实际使用需要加载 Stable Diffusion v1.5 模型进行推理。
当前为演示界面，未加载真实模型权重。"""
    
    return None, info

def build_ui():
    with gr.Blocks(title="Stable Diffusion v1.5 WebUI", theme=gr.themes.Soft()) as app:
        gr.Markdown("# Stable Diffusion v1.5 · 文本生成图像 WebUI")
        gr.Markdown("支持文本到图像生成的演示界面。基于 Stable Diffusion v1.5 模型。")
        
        with gr.Row():
            load_btn = gr.Button("加载模型", variant="primary", size="lg")
            status_tb = gr.Textbox(label="模型状态", value="未加载", interactive=False, lines=4)
        load_btn.click(fn=load_model_click, outputs=status_tb)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 生成参数")
                prompt_input = gr.Textbox(
                    label="提示词 (Prompt)",
                    placeholder="例如：a beautiful landscape with mountains and lakes, sunset, highly detailed",
                    lines=3
                )
                negative_prompt_input = gr.Textbox(
                    label="负面提示词 (Negative Prompt)",
                    placeholder="例如：blurry, low quality, distorted",
                    lines=2
                )
                
                with gr.Row():
                    num_steps = gr.Slider(
                        minimum=10,
                        maximum=100,
                        value=50,
                        step=1,
                        label="采样步数 (Steps)"
                    )
                    guidance_scale = gr.Slider(
                        minimum=1.0,
                        maximum=20.0,
                        value=7.5,
                        step=0.5,
                        label="引导强度 (Guidance Scale)"
                    )
                
                seed_input = gr.Textbox(
                    label="随机种子 (Seed)",
                    value="-1",
                    placeholder="输入数字或留空使用随机种子"
                )
                
                generate_btn = gr.Button("生成图像", variant="primary", size="lg")
            
            with gr.Column(scale=1):
                gr.Markdown("### 生成结果")
                output_image = gr.Image(label="生成的图像", type="pil", height=512)
                output_info = gr.Textbox(label="生成信息", lines=8, interactive=False)
        
        generate_btn.click(
            fn=generate_image,
            inputs=[prompt_input, negative_prompt_input, num_steps, guidance_scale, seed_input],
            outputs=[output_image, output_info]
        )
        
        gr.Markdown("---\n*演示模式：未加载真实模型，结果仅为占位。实际使用需要下载并加载 Stable Diffusion v1.5 模型权重。*")
    
    return app

def main():
    app = build_ui()
    app.launch(server_name="0.0.0.0", server_port=7861, share=False, show_error=True)

if __name__ == "__main__":
    main()