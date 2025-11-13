"""
Knowledge tool for answering questions using FAQ data.
Currently uses simple keyword matching; will be replaced with RAG later.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.settings import FAQ_RAG_FILE, SERVICES_FILE
from utils.logger import log_action, log_error

class KnowledgeTool:
    """Tool for answering user questions using FAQ data."""
    
    def __init__(self):
        """Initialize the KnowledgeTool and load FAQ data."""
        self.faq_data = []
        self.services_data = []
        self._load_faq_data()
    
    def _load_faq_data(self):
        """Load FAQ data from JSON files."""
        try:
            # Load FAQ RAG data
            if FAQ_RAG_FILE.exists():
                with open(FAQ_RAG_FILE, 'r', encoding='utf-8') as f:
                    self.faq_data = json.load(f)
            
            # Load services data
            if SERVICES_FILE.exists():
                with open(SERVICES_FILE, 'r', encoding='utf-8') as f:
                    services_json = json.load(f)
                    self.services_data = services_json.get('services', [])
        except Exception as e:
            print(f"Warning: Could not load FAQ data: {e}")
    
    def _get_hardcoded_answers(self) -> Dict[str, str]:
        """Get hardcoded answers for common questions."""
        return {
            # English
            "what is qiwa": "Qiwa is a comprehensive platform by the Ministry of Human Resources and Social Development in Saudi Arabia that provides employment services for individuals and businesses.",
            "how to register": "To register on Qiwa, visit the official Qiwa website, click on 'Register', choose your account type (Individual, Business, or Service Provider), and follow the registration steps.",
            "what services": "Qiwa provides various services including job search, resume management, recruitment services, employment contracts, work permits, and more.",
            
            # Arabic
            "ما هي منصة قوى": "قوى هي منصة شاملة من وزارة الموارد البشرية والتنمية الاجتماعية في المملكة العربية السعودية توفر خدمات التوظيف للأفراد والشركات.",
            "ما هي قوى": "قوى هي منصة شاملة من وزارة الموارد البشرية والتنمية الاجتماعية في المملكة العربية السعودية توفر خدمات التوظيف للأفراد والشركات.",
            "كيف أسجل": "للتسجيل في منصة قوى، قم بزيارة الموقع الرسمي لقوى، انقر على 'تسجيل'، اختر نوع حسابك (فرد، منشأة، أو مقدم خدمة)، واتبع خطوات التسجيل.",
            "كيف التسجيل": "للتسجيل في منصة قوى، قم بزيارة الموقع الرسمي لقوى، انقر على 'تسجيل'، اختر نوع حسابك (فرد، منشأة، أو مقدم خدمة)، واتبع خطوات التسجيل.",
            "ما الخدمات": "توفر منصة قوى خدمات متنوعة تشمل البحث عن وظائف، إدارة السيرة الذاتية، خدمات التوظيف، عقود العمل، تصاريح العمل، والمزيد."
        }
    
    def _search_faqs(self, query: str, language: str) -> Optional[Dict[str, Any]]:
        """
        Search FAQs using simple keyword matching.
        
        Args:
            query: User query
            language: Language code ('ar' or 'en')
            
        Returns:
            Best matching FAQ or None
        """
        query_lower = query.lower()
        
        # Search in FAQ RAG data
        for faq in self.faq_data:
            faq_text = faq.get('text', '').lower()
            if any(word in faq_text for word in query_lower.split() if len(word) > 3):
                # Extract question and answer from text
                if 'س:' in faq_text and 'ج:' in faq_text:
                    parts = faq_text.split('ج:')
                    if len(parts) == 2:
                        answer = parts[1].strip()
                        return {
                            "answer": answer,
                            "source": "faq_database",
                            "confidence": 0.8,
                            "faq_id": faq.get('id')
                        }
        
        # Search in services data for service-related questions
        for service in self.services_data:
            service_name = service.get('service_name', '').lower()
            description = service.get('description', '').lower()
            
            if any(word in service_name or word in description for word in query_lower.split() if len(word) > 3):
                # Return service information
                answer = f"{service.get('service_name', '')}\n\n{service.get('description', '')}"
                
                # Add steps if available
                steps = service.get('steps', [])
                if steps:
                    answer += f"\n\nالخطوات:\n" + "\n".join(f"- {step}" for step in steps)
                
                return {
                    "answer": answer,
                    "source": "services_database",
                    "confidence": 0.75,
                    "service_id": service.get('id')
                }
        
        return None
    
    def answer_question(
        self,
        userId: str,
        query: str,
        language: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Answer a user question using FAQ data.
        
        Args:
            userId: User identifier
            query: User question
            language: Language code ('ar' or 'en')
            sessionId: Session identifier for logging
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            # Check hardcoded answers first
            hardcoded_answers = self._get_hardcoded_answers()
            query_lower = query.lower().strip()
            
            for question_key, answer in hardcoded_answers.items():
                if question_key in query_lower:
                    result = {
                        "answer": answer,
                        "source": "hardcoded",
                        "confidence": 1.0,
                        "query": query
                    }
                    
                    log_action(
                        sessionId=sessionId,
                        userId=userId,
                        userRole="employee",
                        tool="KnowledgeTool.answer_question",
                        inputs={"userId": userId, "query": query, "language": language},
                        outputs=result
                    )
                    
                    return result
            
            # Search in FAQ database
            faq_result = self._search_faqs(query, language)
            
            if faq_result:
                faq_result["query"] = query
                
                log_action(
                    sessionId=sessionId,
                    userId=userId,
                    userRole="employee",
                    tool="KnowledgeTool.answer_question",
                    inputs={"userId": userId, "query": query, "language": language},
                    outputs=faq_result
                )
                
                return faq_result
            
            # Default response if no match found
            if language == "ar":
                default_answer = "عذراً، لم أتمكن من العثور على إجابة محددة لسؤالك. يمكنك التواصل مع فريق الدعم للمساعدة."
            else:
                default_answer = "I'm sorry, I couldn't find a specific answer to your question. Please contact our support team for assistance."
            
            result = {
                "answer": default_answer,
                "source": "default",
                "confidence": 0.0,
                "query": query
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="KnowledgeTool.answer_question",
                inputs={"userId": userId, "query": query, "language": language},
                outputs=result
            )
            
            return result
            
            # TODO: Replace with RAG vector database query
            # Example implementation:
            # from langchain.vectorstores import Chroma
            # from langchain.embeddings import OpenAIEmbeddings
            # 
            # embeddings = OpenAIEmbeddings()
            # vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
            # docs = vectorstore.similarity_search(query, k=3)
            # 
            # # Use LLM to generate answer from retrieved docs
            # context = "\n\n".join([doc.page_content for doc in docs])
            # answer = call_llm(
            #     system_prompt="You are a helpful assistant for Qiwa platform.",
            #     user_prompt=f"Context: {context}\n\nQuestion: {query}\n\nAnswer:",
            #     sessionId=sessionId
            # )
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="KnowledgeTool.answer_question",
                error=str(e),
                error_type=type(e).__name__
            )
            raise

