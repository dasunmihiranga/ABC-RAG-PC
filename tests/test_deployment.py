import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import main
from core.agent import get_session_history
from core.llm_setup import get_llm


class DeploymentTests(unittest.TestCase):
    def test_health_does_not_initialize_external_services(self):
        with patch.object(main, "get_agent_chain") as create_chain:
            response = TestClient(main.app).get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        create_chain.assert_not_called()

    def test_groq_uses_gpt_oss_by_default(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            with patch.dict(os.environ, {"GROQ_MODEL": ""}):
                os.environ.pop("GROQ_MODEL", None)
                with patch("core.llm_setup.ChatGroq") as chat_groq:
                    get_llm()
        self.assertEqual(chat_groq.call_args.kwargs["model_name"], "openai/gpt-oss-120b")

    def test_production_history_requires_redis(self):
        with patch.dict(os.environ, {"APP_ENV": "production"}):
            with patch.dict(os.environ, {"REDIS_URL": ""}):
                with self.assertRaisesRegex(RuntimeError, "REDIS_URL"):
                    get_session_history("test-session")

    def test_redis_history_selected_when_configured(self):
        with patch.dict(os.environ, {"REDIS_URL": "rediss://example.test:6379/0"}):
            with patch("core.agent.RedisChatMessageHistory") as redis_history:
                get_session_history("test-session")
        self.assertEqual(redis_history.call_args.kwargs["session_id"], "test-session")
        self.assertEqual(redis_history.call_args.kwargs["ttl"], 604800)


if __name__ == "__main__":
    unittest.main()
