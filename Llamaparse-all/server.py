from llama_cloud_services import LlamaExtract
from pydantic import BaseModel, Field, create_model
from typing import List, Optional
import os
import base64
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import tempfile

load_dotenv()

LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
extractor = LlamaExtract()
mcp = FastMCP("llamaparse_dynamic_extract_level_5")

# Helper
def save_pdf(pdf_path: Optional[str], pdf_base64: Optional[str]) -> Optional[str]:
    if pdf_path and os.path.exists(pdf_path):
        return pdf_path
    if pdf_base64:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(base64.b64decode(pdf_base64))
            return f.name
    return None

# === Factory Class ===
class DynamicSchemaFactory:
    @staticmethod
    def build_schema(entities: List[str]) -> type[BaseModel]:
        fields = {
            entity: (str, Field(description=f"{entity} extracted from the document"))
            for entity in entities
        }
        return create_model("DynamicExtractionSchema", **fields)

@mcp.tool()
async def create_agent_and_extract(
    entities: List[str],
    agent_name: str,
    pdf_path: Optional[str] = None,
    pdf_base64: Optional[str] = None
) -> dict:
    path = save_pdf(pdf_path, pdf_base64)
    if not path:
        return {"error": "Provide valid pdf_path or pdf_base64"}

    try:
        schema = DynamicSchemaFactory.build_schema(entities)

        try:
            agent = extractor.get_agent(name=agent_name)
        except:
            agent = extractor.create_agent(name=agent_name, data_schema=schema)

        result = agent.extract(path)
        return {"agent": agent_name, "data": result.data}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if pdf_base64 and os.path.exists(path):
            os.remove(path)

@mcp.tool()
async def get_extraction_result(
    agent_name: str,
    pdf_path: Optional[str] = None,
    pdf_base64: Optional[str] = None
) -> dict:
    path = save_pdf(pdf_path, pdf_base64)
    if not path:
        return {"error": "Provide valid pdf_path or pdf_base64"}
    try:
        agent = extractor.get_agent(name=agent_name)
        result = agent.extract(path)
        return {"data": result.data}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if pdf_base64 and os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
