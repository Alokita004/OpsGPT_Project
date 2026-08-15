📁 Project Structure
OpsGPT/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── agents/
│   │   ├── ops_agent.py
│   │   └── prompts.py
│   │
│   ├── tools/
│   │   ├── anomaly_tools.py
│   │   ├── bigquery_tools.py
│   │   └── remediation_tools.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── pubsub_service.py
│   │   └── cloud_run_service.py
│   │
│   └── utils/
│       └── validators.py
│
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_api.py
│
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
