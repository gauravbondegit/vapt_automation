import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WEB_DIR = os.path.abspath(os.path.dirname(__file__))

CLONED_REPO_DIR = os.path.join(PROJECT_ROOT, "cloned_code")
REPO_STRUCT_PATH = os.path.join(PROJECT_ROOT, "repo_structure.txt")
NODE_RESULTS_DIR = os.path.join(PROJECT_ROOT, "Node_results")
FINAL_REPORT_PATH = os.path.join(PROJECT_ROOT, "VAPT_Final_Report.pdf")

os.makedirs(NODE_RESULTS_DIR, exist_ok=True)


class ScanRequest(BaseModel):
	repo_url: str = Field(..., min_length=1)
	branch_name: str = Field(default="main")
	access_token: str = Field(default="")


def build_initial_state(request: ScanRequest) -> dict:
	return {
		"repo_url": request.repo_url.strip(),
		"branch_name": request.branch_name.strip() or "main",
		"access_token": request.access_token.strip(),
		"repo_path": CLONED_REPO_DIR,
		"file_struct_path": REPO_STRUCT_PATH,
		"node_results": NODE_RESULTS_DIR,
		"messages": [],
		"sender": "",
		"tech_stack": [],
		"final_report": FINAL_REPORT_PATH,
		"v1_msgs": [],
		"v2_msgs": [],
		"v3_msgs": [],
		"v4_msgs": [],
		"v5_msgs": [],
		"v6_msgs": [],
		"v7_msgs": [],
		"v8_msgs": [],
		"v9_msgs": [],
		"v10_msgs": [],
	}


def run_scan(request: ScanRequest) -> dict:
	scan_id = str(uuid.uuid4())

	try:
		from graph import app as workflow_app
	except Exception as error:
		raise HTTPException(status_code=500, detail=f"Failed to load workflow: {error}")

	config = {"configurable": {"thread_id": scan_id}, "recursion_limit": 500}
	initial_state = build_initial_state(request)

	try:
		for event in workflow_app.stream(initial_state, config=config):
			pass

		if not os.path.exists(FINAL_REPORT_PATH):
			raise HTTPException(status_code=500, detail="Workflow ended without generating report")

		return {
			"status": "success",
			"message": "VAPT analysis completed.",
			"report_url": f"/reports/{os.path.basename(FINAL_REPORT_PATH)}",
		}
	except HTTPException:
		raise
	except Exception as error:
		raise HTTPException(status_code=500, detail=str(error))


app = FastAPI(title="VAPT FastAPI Backend", version="1.0.0")


@app.get("/health")
def health_check() -> dict:
	return {"status": "ok"}


@app.post("/perform")
def start_scan(request: ScanRequest) -> dict:
	try:
		return run_scan(request)
	except HTTPException as error:
		return {
			"status": "error",
			"message": str(error.detail),
			"report_url": None,
		}
	except Exception:
		return {
			"status": "error",
			"message": "VAPT analysis could not be completed.",
			"report_url": None,
		}


@app.get("/reports/{report_file_name}")
def get_report(report_file_name: str):
	if report_file_name != os.path.basename(FINAL_REPORT_PATH):
		raise HTTPException(status_code=404, detail="Report file not found")

	if not os.path.exists(FINAL_REPORT_PATH):
		raise HTTPException(status_code=404, detail="Report file missing")

	return FileResponse(
		FINAL_REPORT_PATH,
		media_type="application/pdf",
		filename=os.path.basename(FINAL_REPORT_PATH),
	)


app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="frontend")
