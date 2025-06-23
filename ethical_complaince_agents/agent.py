from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent

# Define individual agents
ethics_agent = LlmAgent(
    name="EthicsAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are an expert in AI ethics. Carefully examine the user's input for potential misuse, moral dilemmas, unsafe behavior, "
        "and ethical red flags, including deception, manipulation, misinformation, or harm to individuals or society. "
        "Flag anything that could cause real-world ethical concern in AI output or usage."
    ),
    description="Analyzes prompts for ethical risks, moral concerns, and potential for misuse or harm."
)

compliance_agent = LlmAgent(
    name="ComplianceAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are an expert legal and policy compliance analyst. Review the input for violations or risks related to regulatory frameworks "
        "such as GDPR, HIPAA, COPPA, EEOC, or corporate policies. Identify issuesnal data exposure, "
        "unauthorized advice, IP infringement, or fa including persoilure to meet fairness and accessibility standards."
    ),
    description="Assesses legal, regulatory, and policy compliance within the prompt."
)

bias_detection_agent = LlmAgent(
    name="BiasDetectionAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are an expert fairness and bias auditor. Examine the input for implicit or explicit bias across gender, race, age, culture, "
        "disability, or socio-economic status. Highlight any stereotyping, exclusionary language, or framing that could lead to "
        "discriminatory outcomes or reinforce harmful narratives."
    ),
    description="Scans prompts for social bias, discrimination, and fairness issues."
)

# Run above agents in parallel
parallel_evaluation = ParallelAgent(
    name="ParallelEvaluationAgent",
    sub_agents=[ethics_agent, compliance_agent, bias_detection_agent],
    description="Runs ethics, compliance, and bias evaluations in parallel."
)

llm_critique_agent = LlmAgent(
    name="LLMCritiqueAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a large language model (LLM) evaluator. Review the analyses from the Ethics, Compliance, and Bias Detection agents. "
        "Provide a constructive critique based on coherence, thoroughness, contradictions, or gaps in reasoning. "
        "Suggest any overlooked issues, contextually relevant improvements, or concerns about prompt quality or safety."
    ),
    description="Performs an expert-level review and critique of prior agent analyses."
)

final_arbiter_agent = LlmAgent(
    name="FinalArbiterAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the final decision-maker. Based on the detailed evaluations from Ethics, Compliance, Bias Detection, and LLM Critique agents, "
        "summarize the key findings and issue one of three final decisions: [SAFE], [RISK], or [BLOCK]. "
        "Be conservative in uncertain cases. Provide a brief rationale that balances ethical, legal, and societal implications."
    ),
    description="Aggregates all agent findings and delivers a final safety classification: SAFE, RISK, or BLOCK."
)


# Define pipeline  (Parallel (Ethics, Compliance, Bias) → Critique → Final Arbiter)
ethical_guard_pipeline = SequentialAgent(
    name="EthicalGuardPipeline",
    sub_agents=[
        parallel_evaluation,
        llm_critique_agent,
        final_arbiter_agent
    ],
    description="Sequentially evaluates prompt using ethical, compliance, bias, and critique agents before final judgment."
)


# Required: Define the root_agent
root_agent = ethical_guard_pipeline
