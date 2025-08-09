import streamlit as st
import pandas as pd
from huggingface_hub import InferenceClient
import pygal
import pdfplumber
import matplotlib.pyplot as plt
import io
import base64
import time
import re
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="PolicyBriefly - AI Regulatory Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.impact-card {
    background: #f8f9ff;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}
.bias-alert {
    background: #fff3cd;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
    margin: 1rem 0;
}
.summary-box {
    background: #d4edda;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏛️ PolicyBriefly</h1>
    <h3>AI-Powered Regulatory Impact Analyzer</h3>
    <p>Transform complex policy documents into actionable business insights</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "policy_text" not in st.session_state:
    st.session_state.policy_text = ""
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API key input
    hf_token = st.text_input("HuggingFace API Token", type="password", help="Get your token from huggingface.co/settings/tokens")
    
    # Analysis options
    st.subheader("Analysis Options")
    include_bias_analysis = st.checkbox("Include Bias Detection", value=True)
    include_impact_scoring = st.checkbox("Include Impact Scoring", value=True)
    summary_length = st.selectbox("Summary Length", ["Short", "Medium", "Detailed"], index=1)
    
    # Sample documents
    st.subheader("📄 Try Sample Documents")
    if st.button("Load EPA Sample"):
        st.session_state.policy_text = """
        ENVIRONMENTAL PROTECTION AGENCY
        40 CFR Part 261
        [EPA-HQ-RCRA-2023-0123; FRL-10234-01]
        RIN 2050-AH45
        
        Hazardous Waste Management System: Definition of Solid Waste
        
        AGENCY: Environmental Protection Agency (EPA).
        ACTION: Final rule.
        
        SUMMARY: The Environmental Protection Agency (EPA) is finalizing amendments to the definition of solid waste under the Resource Conservation and Recovery Act (RCRA). This rule addresses how certain recycled materials are regulated under RCRA's hazardous waste regulations. The final rule will reduce regulatory burden on legitimate recycling while maintaining environmental protection.
        
        DATES: This rule is effective January 1, 2024.
        
        SUPPLEMENTARY INFORMATION:
        I. Background
        The current regulations create uncertainty for recyclers and manufacturers about when recycled materials are subject to hazardous waste regulations. This final rule provides clarity by establishing clear criteria for determining when recycled materials are solid wastes subject to RCRA Subtitle C regulations.
        
        II. Final Rule
        Under this final rule, recycled materials will be considered solid waste unless they meet specific exclusion criteria. The rule establishes a framework for legitimate recycling that considers factors such as:
        - Whether the recycling process is legitimate
        - Whether hazardous secondary materials are managed as valuable commodities
        - Whether the recycling process results in a valuable product
        
        III. Economic Impact
        EPA estimates this rule will result in cost savings of $54 million annually for the recycling industry while maintaining equivalent environmental protection. Small businesses will particularly benefit from reduced compliance costs.
        """
        st.success("EPA sample loaded!")

# Core analysis functions
def initialize_client(token):
    """Initialize HuggingFace inference client"""
    if not token:
        return None
    try:
        return InferenceClient(token=token)
    except Exception as e:
        st.error(f"Failed to initialize client: {str(e)}")
        return None

def extract_key_sections(text):
    """Extract key sections from policy document"""
    sections = {}
    
    # Common policy document sections
    patterns = {
        "summary": r"SUMMARY:?\s*(.*?)(?=\n[A-Z][A-Z\s]+:|$)",
        "background": r"BACKGROUND:?\s*(.*?)(?=\n[A-Z][A-Z\s]+:|$)",
        "dates": r"DATES?:?\s*(.*?)(?=\n[A-Z][A-Z\s]+:|$)",
        "economic_impact": r"ECONOMIC IMPACT:?\s*(.*?)(?=\n[A-Z][A-Z\s]+:|$)",
        "effective_date": r"(?:effective|EFFECTIVE).*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}|\w+ \d{1,2}, \d{4})",
    }
    
    for section, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section] = match.group(1).strip()[:500]  # Limit length
    
    return sections

def analyze_policy_with_fallback(text, client=None):
    """Analyze policy with fallback to rule-based analysis if API fails"""
    
    # Extract key sections
    sections = extract_key_sections(text)
    
    # Fallback analysis (rule-based) if no client
    if not client:
        return create_fallback_analysis(text, sections)
    
    try:
        # Try AI analysis first
        return analyze_with_ai(text, sections, client)
    except Exception as e:
        st.warning(f"AI analysis failed ({str(e)}), using fallback analysis")
        return create_fallback_analysis(text, sections)

def analyze_with_ai(text, sections, client):
    """AI-powered analysis using HuggingFace models"""
    
    # Truncate text for API limits
    text_snippet = text[:2000]
    
    results = {
        "summary": "",
        "bias_analysis": {},
        "impact_scores": {},
        "key_dates": [],
        "stakeholders": []
    }
    
    # Generate summary
    try:
        summary_prompt = f"Summarize this policy document in plain business language, focusing on practical impacts:\n\n{text_snippet}"
        summary_response = client.text_generation(
            summary_prompt,
            model="microsoft/DialoGPT-medium",  # Using available model
            max_new_tokens=200
        )
        results["summary"] = summary_response
    except:
        results["summary"] = create_rule_based_summary(text, sections)
    
    # Bias analysis
    if sections:
        bias_indicators = analyze_bias_patterns(text)
        results["bias_analysis"] = bias_indicators
    
    # Impact scoring
    results["impact_scores"] = calculate_impact_scores(text, sections)
    
    # Extract dates and stakeholders
    results["key_dates"] = extract_dates(text)
    results["stakeholders"] = extract_stakeholders(text)
    
    return results

def create_fallback_analysis(text, sections):
    """Rule-based fallback analysis"""
    
    results = {
        "summary": create_rule_based_summary(text, sections),
        "bias_analysis": analyze_bias_patterns(text),
        "impact_scores": calculate_impact_scores(text, sections),
        "key_dates": extract_dates(text),
        "stakeholders": extract_stakeholders(text)
    }
    
    return results

def create_rule_based_summary(text, sections):
    """Create summary using rule-based approach"""
    
    if "summary" in sections:
        return f"**Key Points:** {sections['summary'][:300]}..."
    
    # Extract first few sentences
    sentences = re.split(r'[.!?]+', text)
    key_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
    
    summary = " ".join(key_sentences)
    if len(summary) > 400:
        summary = summary[:400] + "..."
    
    return summary

def analyze_bias_patterns(text):
    """Analyze potential bias patterns in the document"""
    
    bias_indicators = {
        "language_bias": 0,
        "stakeholder_bias": 0,
        "economic_bias": 0,
        "details": []
    }
    
    # Language bias indicators
    positive_words = ["benefit", "improve", "enhance", "opportunity", "growth"]
    negative_words = ["burden", "costly", "difficult", "challenge", "restrict"]
    
    text_lower = text.lower()
    pos_count = sum(text_lower.count(word) for word in positive_words)
    neg_count = sum(text_lower.count(word) for word in negative_words)
    
    if pos_count > neg_count * 2:
        bias_indicators["language_bias"] = 0.7
        bias_indicators["details"].append("Document uses predominantly positive language")
    elif neg_count > pos_count * 2:
        bias_indicators["language_bias"] = 0.8
        bias_indicators["details"].append("Document uses predominantly negative language")
    
    # Stakeholder bias
    business_terms = ["industry", "business", "company", "economic"]
    public_terms = ["citizen", "public", "community", "environmental"]
    
    business_count = sum(text_lower.count(term) for term in business_terms)
    public_count = sum(text_lower.count(term) for term in public_terms)
    
    if business_count > public_count * 2:
        bias_indicators["stakeholder_bias"] = 0.6
        bias_indicators["details"].append("Document appears to favor business interests")
    elif public_count > business_count * 2:
        bias_indicators["stakeholder_bias"] = 0.6
        bias_indicators["details"].append("Document appears to favor public interests")
    
    return bias_indicators

def calculate_impact_scores(text, sections):
    """Calculate various impact scores"""
    
    scores = {
        "compliance_complexity": 0,
        "cost_impact": 0,
        "timeline_urgency": 0,
        "scope_breadth": 0
    }
    
    text_lower = text.lower()
    
    # Compliance complexity
    complex_terms = ["requirement", "shall", "must", "compliance", "regulation", "standard"]
    complexity_score = min(sum(text_lower.count(term) for term in complex_terms) / 10, 1.0)
    scores["compliance_complexity"] = complexity_score
    
    # Cost impact
    cost_terms = ["cost", "fee", "penalty", "fine", "expense", "budget"]
    cost_score = min(sum(text_lower.count(term) for term in cost_terms) / 5, 1.0)
    scores["cost_impact"] = cost_score
    
    # Timeline urgency
    urgent_terms = ["immediate", "within", "days", "effective", "deadline"]
    urgency_score = min(sum(text_lower.count(term) for term in urgent_terms) / 8, 1.0)
    scores["timeline_urgency"] = urgency_score
    
    # Scope breadth
    scope_terms = ["all", "every", "entire", "comprehensive", "broad", "wide"]
    scope_score = min(sum(text_lower.count(term) for term in scope_terms) / 6, 1.0)
    scores["scope_breadth"] = scope_score
    
    return scores

def extract_dates(text):
    """Extract important dates from the document"""
    
    date_patterns = [
        r'\b(\w+ \d{1,2}, \d{4})\b',
        r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})\b',
        r'\b(\d{4}-\d{2}-\d{2})\b'
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        dates.extend(matches)
    
    return list(set(dates))[:5]  # Return unique dates, max 5

def extract_stakeholders(text):
    """Extract stakeholders mentioned in the document"""
    
    stakeholder_patterns = [
        r'\b(businesses?|companies|corporations?|firms?)\b',
        r'\b(citizens?|public|communities?|consumers?)\b',
        r'\b(government|agencies?|departments?)\b',
        r'\b(environmental groups?|advocacy|organizations?)\b'
    ]
    
    stakeholders = set()
    text_lower = text.lower()
    
    for pattern in stakeholder_patterns:
        matches = re.findall(pattern, text_lower)
        stakeholders.update(matches)
    
    return list(stakeholders)[:8]

def create_impact_visualization(scores):
    """Create impact score visualization using pygal"""
    
    # Create radar chart
    radar_chart = pygal.Radar()
    radar_chart.title = 'Policy Impact Assessment'
    radar_chart.x_labels = [
        'Compliance Complexity',
        'Cost Impact', 
        'Timeline Urgency',
        'Scope Breadth'
    ]
    
    # Convert scores to percentages
    score_values = [
        scores.get('compliance_complexity', 0) * 100,
        scores.get('cost_impact', 0) * 100,
        scores.get('timeline_urgency', 0) * 100,
        scores.get('scope_breadth', 0) * 100
    ]
    
    radar_chart.add('Impact Level', score_values)
    
    return radar_chart.render_data_uri()

def create_timeline_chart(dates):
    """Create timeline visualization"""
    
    if not dates:
        return None
    
    line_chart = pygal.DateTimeLine(
        title="Key Policy Timeline",
        x_label_rotation=35,
        truncate_label=-1,
    )
    
    # For demo, create sample timeline data
    timeline_data = [
        (datetime.now() + timedelta(days=30), 'Public Comment Period Ends'),
        (datetime.now() + timedelta(days=90), 'Implementation Phase'),
        (datetime.now() + timedelta(days=180), 'Full Compliance Required')
    ]
    
    for date, event in timeline_data:
        line_chart.add(event, [(date, 1)])
    
    return line_chart.render_data_uri()

# File upload section
st.subheader("📁 Upload Policy Document")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose a policy document", 
        type=["pdf", "txt"],
        help="Upload PDF or TXT files containing policy documents"
    )

with col2:
    st.markdown("**Supported formats:**")
    st.markdown("• PDF documents")
    st.markdown("• Plain text files")
    st.markdown("• Government policy docs")

# Document processing
if uploaded_file is not None:
    with st.spinner("📖 Extracting document content..."):
        try:
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            else:
                text = uploaded_file.read().decode("utf-8")
            
            st.session_state.policy_text = text
            
            # Show document preview
            with st.expander("📄 Document Preview", expanded=False):
                st.text_area("Content Preview", text[:1000] + "..." if len(text) > 1000 else text, height=200)
            
            st.success(f"✅ Document extracted successfully! ({len(text)} characters)")
            
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")

# Analysis section
if st.session_state.policy_text:
    st.subheader("🔍 Policy Analysis")
    
    if st.button("🚀 Analyze Document", type="primary"):
        
        # Initialize client
        client = initialize_client(hf_token) if hf_token else None
        
        with st.spinner("🤖 Analyzing policy document..."):
            progress_bar = st.progress(0)
            
            # Simulate progress
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Perform analysis
            results = analyze_policy_with_fallback(st.session_state.policy_text, client)
            st.session_state.analysis_results = results
            
            progress_bar.empty()
            st.success("✅ Analysis complete!")

# Display results
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # Summary section
    st.subheader("📋 Executive Summary")
    st.markdown(f"""
    <div class="summary-box">
    <h4>🎯 Key Findings</h4>
    <p>{results['summary']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Impact scoring
    if include_impact_scoring and results.get('impact_scores'):
        st.subheader("📊 Impact Assessment")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create and display radar chart
            chart_uri = create_impact_visualization(results['impact_scores'])
            if chart_uri:
                st.markdown(f'<img src="{chart_uri}" width="100%">', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Impact Scores:**")
            for score_name, score_value in results['impact_scores'].items():
                score_percentage = int(score_value * 100)
                score_display = score_name.replace('_', ' ').title()
                
                # Color coding
                if score_percentage >= 70:
                    color = "🔴"
                elif score_percentage >= 40:
                    color = "🟡"
                else:
                    color = "🟢"
                
                st.markdown(f"{color} **{score_display}:** {score_percentage}%")
    
    # Bias analysis
    if include_bias_analysis and results.get('bias_analysis'):
        st.subheader("⚖️ Bias Analysis")
        
        bias_data = results['bias_analysis']
        
        if bias_data.get('details'):
            for detail in bias_data['details']:
                st.markdown(f"""
                <div class="bias-alert">
                <strong>⚠️ Potential Bias Detected:</strong> {detail}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="impact-card">
            <strong>✅ No significant bias patterns detected</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Key information
    col1, col2 = st.columns(2)
    
    with col1:
        if results.get('key_dates'):
            st.subheader("📅 Important Dates")
            for date in results['key_dates']:
                st.markdown(f"• {date}")
    
    with col2:
        if results.get('stakeholders'):
            st.subheader("👥 Stakeholders")
            for stakeholder in results['stakeholders']:
                st.markdown(f"• {stakeholder.title()}")
    
    # Export options
    st.subheader("📤 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report"):
            st.info("PDF generation feature coming soon!")
    
    with col2:
        # JSON export
        json_data = json.dumps(results, indent=2)
        st.download_button(
            label="📊 Download JSON",
            data=json_data,
            file_name=f"policy_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col3:
        if st.button("📧 Email Summary"):
            st.info("Email integration coming soon!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
<p>PolicyBriefly v1.0 | Built with ❤️ using Streamlit & HuggingFace</p>
<p>Transform complex policies into actionable insights</p>
</div>
""", unsafe_allow_html=True)
