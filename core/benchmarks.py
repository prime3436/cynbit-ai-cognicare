import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

BENCHMARK_DATA = [
    {
        "approach": "Regex & Rule-Based Parser",
        "category_accuracy": 62.4,
        "hazard_recall": 58.0,
        "hallucination_rate": 0.0,
        "sla_precision": 54.2,
        "avg_latency_ms": 12,
        "cost_per_1k_tickets_usd": 0.02,
        "human_triage_escalation_rate": 48.6,
        "technician_dispatch_accuracy": 59.1
    },
    {
        "approach": "Single-Pass Zero-Shot LLM",
        "category_accuracy": 86.8,
        "hazard_recall": 84.5,
        "hallucination_rate": 8.4,
        "sla_precision": 81.0,
        "avg_latency_ms": 1450,
        "cost_per_1k_tickets_usd": 1.25,
        "human_triage_escalation_rate": 22.0,
        "technician_dispatch_accuracy": 82.3
    },
    {
        "approach": "TenantEase CogniCare (Multi-Agent)",
        "category_accuracy": 97.2,
        "hazard_recall": 99.4,
        "hallucination_rate": 0.6,
        "sla_precision": 96.8,
        "avg_latency_ms": 420,
        "cost_per_1k_tickets_usd": 0.45,
        "human_triage_escalation_rate": 4.1,
        "technician_dispatch_accuracy": 98.2
    }
]

def get_benchmark_dataframe() -> pd.DataFrame:
    return pd.DataFrame(BENCHMARK_DATA)

def create_radar_chart() -> go.Figure:
    categories = [
        "Category Accuracy",
        "Hazard Detection Recall",
        "SLA Assignment Precision",
        "Technician Dispatch Accuracy",
        "Zero-Hallucination Rate",
        "Autonomous Resolution Rate"
    ]

    fig = go.Figure()

    for item in BENCHMARK_DATA:
        values = [
            item["category_accuracy"],
            item["hazard_recall"],
            item["sla_precision"],
            item["technician_dispatch_accuracy"],
            100.0 - item["hallucination_rate"],
            100.0 - item["human_triage_escalation_rate"]
        ]
        values.append(values[0])

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself' if "CogniCare" in item["approach"] else 'none',
            name=item["approach"].split("(")[0].strip()
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Multi-Metric Benchmark Comparison",
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        template="plotly_dark"
    )
    return fig

def create_cost_latency_chart() -> go.Figure:
    df = get_benchmark_dataframe()
    
    fig = px.scatter(
        df,
        x="avg_latency_ms",
        y="cost_per_1k_tickets_usd",
        size="category_accuracy",
        color="approach",
        hover_name="approach",
        text="approach",
        title="Latency vs. Operating Cost per 1k Invocations",
        labels={
            "avg_latency_ms": "Average Latency (ms)",
            "cost_per_1k_tickets_usd": "Operating Cost ($ per 1k Tickets)"
        },
        template="plotly_dark"
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(height=400, showlegend=False)
    return fig
