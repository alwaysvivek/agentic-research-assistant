# Reliable Researcher - Local Agentic RAG

> **A local, privacy-focused AI research assistant that uses self-correcting agentic workflows to provide reliable answers from your documents.**

![Dashboard](image.png)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

---

## 🎯 Overview

Reliable Researcher is an AI application that combines **Retrieval-Augmented Generation (RAG)** with **agentic workflows** powered by LangGraph. It ingests content from multiple sources (URLs, PDFs, raw text), stores embeddings locally, and uses a self-correcting agent to generate high-confidence answers.

### Key Features

- ✨ **Agentic RAG Workflow**: Self-correcting retrieve-grade-generate loop using LangGraph
- 📚 **Multi-Source Ingestion**: Support for URLs, PDF uploads, and raw text
- 🎯 **Confidence Scoring**: Transparent reliability metrics for each answer
- 🗄️ **Local Vector Database**: Serverless LanceDB for efficient embedding storage (Local)
- 🔒 **Privacy Focused**: Your data stays local. API Keys are stored in your browser.
- 🐳 **Easy Setup**: Single command startup with Docker Compose.

### Gallery
| | |
|:-------------------------:|:-------------------------:|
| ![Ingestion](image%20copy.png) | ![Research](image%20copy%202.png) |
| ![Results](image%20copy%203.png) | |

---

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** installed and running.
- **Groq API Key** ([Get one here](https://console.groq.com/keys)) for the LLM.

### Run the Application

1. **Clone & Build**
   ```bash
   git clone https://github.com/alwaysvivek/agentic-research-assistant.git
   cd agentic-research-assistant
   
   # Build and start the services
   docker-compose up --build
   ```

2. **Access the App**
   - Open your browser to **[http://localhost:5173](http://localhost:5173)**.
   - You will be prompted to enter your **Groq API Key** on startup.
   - The key is stored locally in your browser and used for research queries.

3. **Stop the App**
   ```bash
   docker-compose down
   ```

---

## 🏗️ Architecture

```mermaid
graph TB
    %% Nodes
    subgraph "Frontend (React + Vite)"
        Client["Browser / User"]
        Store["LocalStorage (API Key)"]
        UI_Ingest[Ingest Component]
        UI_Chat[Chat Interface]
    end

    subgraph "Backend Service (FastAPI)"
        API_Gateway[API Router / Rate Limiter]
        
        subgraph "Ingestion Pipeline"
            Loader["Document Loaders<br>(PDF/Web/Text)"]
            Splitter[Text Splitter]
            Embedder["HuggingFace Embeddings<br>(Local Model)"]
        end

        subgraph "Agentic Core (LangGraph)"
            Graph[StateGraph Controller]
            Retrieve["Retrieve Node<br>(LanceDB Retriever)"]
            Generate["Generate Node<br>(ChatGroq + Prompts)"]
            Grade{"Confidence Check<br>(> 0.7 or Max Tries)"}
        end
    end

    subgraph "Data Storage"
        VectorDB[("LanceDB<br>Vector Store")]
        FileSystem[Temp File Storage]
    end

    subgraph "External AI Services"
        GroqAPI["Groq API<br>(Llama 3.3-70b)"]
    end

    %% Flows - Frontend to Backend
    Client --> UI_Ingest
    Client --> UI_Chat
    Store -.->|Inject API Key| UI_Chat
    UI_Ingest -->|POST /ingest| API_Gateway
    UI_Chat -->|POST /research| API_Gateway

    %% Flows - Ingestion
    API_Gateway -->|Source/File| Loader
    Loader --> Splitter
    Splitter --> Embedder
    Embedder -->|Vectors| VectorDB
    Loader -.->|Temp PDF| FileSystem

    %% Flows - Research
    API_Gateway -->|Query + Key| Graph
    Graph --> Retrieve
    Retrieve -->|Query| VectorDB
    VectorDB -->|Context Chunks| Retrieve
    Retrieve --> Generate
    Generate -->|Context + Query| GroqAPI
    GroqAPI -->|Answer + Confidence| Generate
    Generate --> Grade
    Grade -->|Retry (Target < 0.7)| Retrieve
    Grade -->|Success (Target > 0.7)| API_Gateway

    %% Styling
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef backend fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef data fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef ai fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    
    class Client,Store,UI_Ingest,UI_Chat frontend;
    class API_Gateway,Loader,Splitter,Embedder,Graph,Retrieve,Generate,Grade backend;
    class VectorDB,FileSystem data;
    class GroqAPI ai;
```

## 🛠️ Tech Stack

- **Backend Framework**: Python (FastAPI)
- **Agentic AI**: LangGraph (State Control), LangChain (Orchestration)
- **LLM Provider**: Groq API (Llama 3.3-70b-versatile)
- **Vector Database**: LanceDB (Serverless High-Performance Vector Store)
- **Embeddings**: HuggingFace (Local Execution, no API cost)
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS
- **Infrastructure**: Docker & Docker Compose

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
