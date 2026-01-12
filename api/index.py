"""
Vercel Serverless Function 入口点
用于部署到 Vercel 平台
"""

from src.app import app

# Vercel 会自动调用这个 handler
handler = app
