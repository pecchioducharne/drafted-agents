"""
Core interfaces for extensibility.

These define the three key "extension seams":
1. Skill interface - add capabilities without rewiring
2. Executor interface - swap execution backends
3. JobType interface - add new workflows cleanly
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# EXTENSIBILITY SEAM #1: Skill Interface
# ============================================================================

class SkillStatus(Enum):
    """Skill execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class SkillResult:
    """Standard skill execution result"""
    status: SkillStatus
    outputs: Dict[str, Any]
    artifacts: Dict[str, str]  # name -> path/url
    logs: List[str]
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class Skill(ABC):
    """
    Base skill interface.
    
    All skills must implement this contract.
    New integrations = new skill module + optional tool client.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique skill identifier"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description"""
        pass
    
    @property
    @abstractmethod
    def inputs_schema(self) -> Dict[str, Any]:
        """JSON schema for required inputs"""
        pass
    
    @property
    @abstractmethod
    def outputs_schema(self) -> Dict[str, Any]:
        """JSON schema for expected outputs"""
        pass
    
    @property
    @abstractmethod
    def allowed_tools(self) -> List[str]:
        """List of tools this skill can use"""
        pass
    
    @property
    @abstractmethod
    def success_checks(self) -> List[str]:
        """List of conditions that must be true for success"""
        pass
    
    @abstractmethod
    async def run(self, context: "TaskContext") -> SkillResult:
        """
        Execute the skill with given context.
        
        Args:
            context: TaskContext with inputs and state
            
        Returns:
            SkillResult with outputs, artifacts, logs
        """
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate inputs against schema (optional override)"""
        # TODO: Implement JSON schema validation
        return True


# ============================================================================
# EXTENSIBILITY SEAM #2: Executor Interface
# ============================================================================

class ExecutorStatus(Enum):
    """Executor run status"""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutorArtifacts:
    """Standard artifacts returned by executors"""
    patch: Optional[str] = None
    pr_url: Optional[str] = None
    logs: List[str] = None
    test_report: Dict[str, Any] = None
    deploy_url: Optional[str] = None
    files_changed: List[str] = None


class Executor(ABC):
    """
    Base executor interface.
    
    Swap between OpenHands / Claude Code / Codex without changing orchestrator.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Executor identifier (e.g., 'openhands', 'claude_code')"""
        pass
    
    @abstractmethod
    async def start(self, task: Dict[str, Any]) -> str:
        """
        Start execution of a task.
        
        Args:
            task: Task specification with repo, instruction, constraints
            
        Returns:
            run_id for tracking
        """
        pass
    
    @abstractmethod
    async def get_status(self, run_id: str) -> ExecutorStatus:
        """Get current status of a run"""
        pass
    
    @abstractmethod
    async def stream_logs(self, run_id: str) -> AsyncIterator[str]:
        """Stream logs from the executor"""
        pass
    
    @abstractmethod
    async def get_artifacts(self, run_id: str) -> ExecutorArtifacts:
        """Get all artifacts produced by the run"""
        pass
    
    @abstractmethod
    async def cancel(self, run_id: str) -> bool:
        """Cancel a running execution"""
        pass


from typing import AsyncIterator  # Import after class definition to avoid forward ref issue


# ============================================================================
# EXTENSIBILITY SEAM #3: Job Type Template
# ============================================================================

@dataclass
class JobGate:
    """Gate that must pass before proceeding"""
    name: str
    condition: str  # e.g., "tests_pass", "manual_approval"
    required: bool = True
    timeout_seconds: Optional[int] = None


@dataclass
class SkillStep:
    """A step in a job workflow"""
    skill_name: str
    inputs: Dict[str, Any]
    optional: bool = False
    retry_count: int = 0
    timeout_seconds: Optional[int] = None


@dataclass
class JobType:
    """
    Job type template - defines an async workflow.
    
    New workflow = new config file with this structure.
    """
    name: str
    description: str
    required_persona: str
    skills_sequence: List[SkillStep]  # Ordered list or parallel groups
    gates: List[JobGate]
    retry_policy: Dict[str, Any]
    metadata: Dict[str, Any]


# ============================================================================
# Task Context (standard contract)
# ============================================================================

@dataclass
class TaskContext:
    """
    Standard task context used by all jobs.
    
    This is the contract that every job, skill, and executor uses.
    """
    task_id: str
    job_type: str
    request: str
    
    # Inputs
    repo: Optional[str] = None
    issue: Optional[str] = None
    pr: Optional[str] = None
    constraints: List[str] = None
    
    # Routing
    persona: Optional[str] = None
    skills: List[str] = None
    executor: Optional[str] = None
    
    # State
    status: str = "pending"
    current_step: Optional[str] = None
    artifacts: Dict[str, Any] = None
    outputs: Dict[str, Any] = None
    
    # Context
    github_context: Dict[str, Any] = None
    netlify_context: Dict[str, Any] = None
    firebase_context: Dict[str, Any] = None
    
    # Metadata
    created_at: str = None
    updated_at: str = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []
        if self.skills is None:
            self.skills = []
        if self.artifacts is None:
            self.artifacts = {}
        if self.outputs is None:
            self.outputs = {}
        if self.metadata is None:
            self.metadata = {}


# ============================================================================
# Skill Registry
# ============================================================================

class SkillRegistry:
    """
    Central registry for skills.
    
    Add new skills without modifying the router - just register them.
    """
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
    
    def register(self, skill: Skill):
        """Register a new skill"""
        self._skills[skill.name] = skill
    
    def get(self, name: str) -> Optional[Skill]:
        """Get skill by name"""
        return self._skills.get(name)
    
    def list_all(self) -> List[str]:
        """List all registered skill names"""
        return list(self._skills.keys())
    
    def get_skills_by_tool(self, tool: str) -> List[Skill]:
        """Find skills that use a specific tool"""
        return [
            skill for skill in self._skills.values()
            if tool in skill.allowed_tools
        ]


# ============================================================================
# Executor Registry
# ============================================================================

class ExecutorRegistry:
    """
    Central registry for executors.
    
    Swap execution backends by changing routing rules.
    """
    
    def __init__(self):
        self._executors: Dict[str, Executor] = {}
        self._default: Optional[str] = None
    
    def register(self, executor: Executor, is_default: bool = False):
        """Register a new executor"""
        self._executors[executor.name] = executor
        if is_default or self._default is None:
            self._default = executor.name
    
    def get(self, name: Optional[str] = None) -> Optional[Executor]:
        """Get executor by name, or default if name is None"""
        if name is None:
            name = self._default
        return self._executors.get(name)
    
    def list_all(self) -> List[str]:
        """List all registered executor names"""
        return list(self._executors.keys())
