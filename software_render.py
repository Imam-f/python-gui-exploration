import os
import sys
from OpenGL.GL import *
import pygame
from pygame.locals import *

class RendererTester:
    def __init__(self):
        self.renderers_to_test = [
            {'name': 'Default', 'env': {}},
            {'name': 'Software', 'env': {'LIBGL_ALWAYS_SOFTWARE': '1'}},
            {'name': 'NVIDIA', 'env': {'__NV_PRIME_RENDER_OFFLOAD': '1'}},
            {'name': 'AMD', 'env': {'DRI_PRIME': '1'}},
        ]
        
    def test_renderer(self, env_vars):
        """Test specific renderer configuration"""
        # Save original environment
        old_environ = dict(os.environ)
        
        try:
            # Apply test environment
            os.environ.update(env_vars)
            
            # Initialize PyGame with OpenGL
            pygame.init()
            pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
            
            # Get renderer info
            renderer = glGetString(GL_RENDERER).decode()
            vendor = glGetString(GL_VENDOR).decode()
            version = glGetString(GL_VERSION).decode()
            
            print(f"Renderer: {renderer}")
            print(f"Vendor: {vendor}")
            print(f"Version: {version}")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pygame.quit()
            # Restore original environment
            os.environ.clear()
            os.environ.update(old_environ)
    
    def run_tests(self):
        """Test all renderer configurations"""
        print("Testing OpenGL Renderer Configurations")
        print("=====================================")
        
        for config in self.renderers_to_test:
            print(f"\nTesting {config['name']} configuration:")
            print("-" * 40)
            self.test_renderer(config['env'])

if __name__ == "__main__":
    tester = RendererTester()
    tester.run_tests()