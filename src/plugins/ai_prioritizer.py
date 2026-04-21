from src.plugins.base import BasePlugin
from datetime import datetime

class AIPrioritizerPlugin(BasePlugin):
    def execute(self, manager):
        for task in manager.tasks.values():
            score = 0
            
            # 1. Keyword Check (Urgency)
            urgency_words = ["critical", "urgent", "asap", "important"]
            if any(word in task.title.lower() for word in urgency_words):
                score += 3
            
            # 2. Dependency Impact
            dependents = [t for t in manager.tasks.values() if task.id in t.dependencies]
            score += len(dependents) * 2
            
            # 3. Deadline Proximity
            if task.deadline:
                try:
                    due = datetime.fromisoformat(task.deadline)
                    days_left = (due - datetime.now()).days
                    if days_left < 3:
                        score += 5
                    elif days_left < 7:
                        score += 2
                except ValueError:
                    pass
            
            task.priority = min(score, 10)
