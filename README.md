# 🏛️ PolicyBriefly - AI-Powered Regulatory Impact Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://huggingface.co/spaces/your-username/PolicyBriefly)

## 🚀 Overview

PolicyBriefly is an AI-powered web application that transforms complex government policy documents into clear, actionable business insights. It analyzes regulatory documents and provides:

- **Plain-English Summaries**: Convert legal jargon into business-friendly language
- **Impact Assessment**: Quantify compliance complexity, cost impact, timeline urgency, and scope
- **Bias Detection**: Identify potential biases in policy language and stakeholder treatment
- **Visual Analytics**: Interactive charts and scorecards for executive presentations
- **Export Options**: Download analysis results in multiple formats

## ✨ Key Features

### 🤖 AI-Powered Analysis
- **Dual Model Approach**: Uses HuggingFace models for summarization and bias detection
- **Fallback Analysis**: Rule-based analysis when AI models are unavailable
- **Smart Text Extraction**: Supports PDF and TXT document formats

### 📊 Visual Impact Reports
- **Impact Scorecards**: Radar charts showing compliance complexity, cost impact, urgency, and scope
- **Timeline Visualization**: Key dates and implementation milestones
- **Bias Indicators**: Visual alerts for potential bias patterns

### 🎯 Business-Ready Outputs
- **Executive Summaries**: Concise, actionable insights for decision-makers
- **Stakeholder Analysis**: Identify affected parties and interest groups
- **Compliance Roadmap**: Extract important dates and deadlines

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based web framework)
- **AI Models**: HuggingFace Inference API
- **Visualization**: Pygal for interactive charts
- **Document Processing**: PDFPlumber for PDF text extraction
- **Deployment**: Ready for HuggingFace Spaces

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/PolicyBriefly.git
   cd PolicyBriefly
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

### HuggingFace Spaces Deployment

1. **Create a new Space** on [HuggingFace Spaces](https://huggingface.co/spaces)
2. **Select Streamlit** as the SDK
3. **Upload files** or connect your GitHub repository
4. **Add your HuggingFace token** in the Spaces settings (optional for enhanced AI features)

## 📁 Project Structure

```
PolicyBriefly/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore           # Git ignore file
```

## 🔧 Configuration

### HuggingFace API Token (Optional)
For enhanced AI analysis features, you can provide a HuggingFace API token:

1. Get your token from [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Enter it in the sidebar configuration panel
3. The app works without a token using fallback rule-based analysis

### Analysis Options
- **Bias Detection**: Toggle bias analysis on/off
- **Impact Scoring**: Enable/disable impact assessment
- **Summary Length**: Choose between Short, Medium, or Detailed summaries

## 📊 Sample Analysis

Try the built-in EPA sample document to see PolicyBriefly in action:

1. Click "Load EPA Sample" in the sidebar
2. Click "🚀 Analyze Document"
3. View the comprehensive analysis results

## 🎯 Use Cases

### For Legal Teams
- **Compliance Assessment**: Understand new regulatory requirements
- **Risk Analysis**: Identify potential compliance risks and costs
- **Timeline Planning**: Extract key dates and implementation deadlines

### For Business Executives
- **Impact Summaries**: Get executive-level overviews of regulatory changes
- **Strategic Planning**: Understand how policies affect business operations
- **Stakeholder Communication**: Share clear, visual impact reports

### For Policy Researchers
- **Bias Analysis**: Identify potential biases in policy language
- **Comparative Analysis**: Compare multiple policy documents
- **Data Export**: Download analysis results for further research

## 🔍 Analysis Components

### Impact Scoring
- **Compliance Complexity**: How difficult is it to comply?
- **Cost Impact**: What are the financial implications?
- **Timeline Urgency**: How quickly must you act?
- **Scope Breadth**: How widely does this apply?

### Bias Detection
- **Language Bias**: Positive vs. negative language patterns
- **Stakeholder Bias**: Fair representation of different groups
- **Economic Bias**: Balance between business and public interests

### Key Extraction
- **Important Dates**: Deadlines, effective dates, milestones
- **Stakeholders**: Affected parties and interest groups
- **Requirements**: Key compliance obligations

## 🚀 Future Enhancements

- [ ] **PDF Report Generation**: Export comprehensive PDF reports
- [ ] **Email Integration**: Send analysis summaries via email
- [ ] **Multi-language Support**: Analyze policies in different languages
- [ ] **Compliance Tracking**: Monitor deadlines and requirements
- [ ] **Database Integration**: Connect to real-time policy databases
- [ ] **Collaborative Features**: Team sharing and annotations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HuggingFace**: For providing excellent AI model infrastructure
- **Streamlit**: For the amazing web framework
- **Pygal**: For beautiful, interactive visualizations
- **PDFPlumber**: For robust PDF text extraction

## 📞 Support

For questions, suggestions, or issues:
- Open an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [Project Wiki](https://github.com/your-username/PolicyBriefly/wiki)

---

**Built with ❤️ for making policy analysis accessible to everyone**