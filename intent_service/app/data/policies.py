POLICIES = {
    "account_inquiry": "For account inquiries, agents must verify the customer's identity by asking for at least two pieces of identifying information before providing any balance or transactional details.",
    "loan_inquiry": "For loan inquiries, provide information regarding current rates and standard eligibility requirements. Do not guarantee approval. For specific application processes, direct the customer to the online portal.",
    "transaction_dispute": "For transaction disputes, inform the customer that disputes must be filed within 60 days of the statement date. Ensure they have the merchant name, date, and amount ready.",
    "card_issue": "For issues related to lost or stolen cards, immediately offer to block the card to prevent unauthorized use. Outline the timeline for receiving a replacement card (typically 3-5 business days).",
    "general_inquiry": "For general inquiries, provide polite, helpful assistance focusing on branch hours, locations, or available services. If the question requires specific financial advice, route the customer to a specialist."
}

def get_policy(intent: str) -> str:
    return POLICIES.get(intent, "No specific policy retrieved for this intent. Please follow general banking guidelines: prioritize customer security, privacy, and polite assistance.")
