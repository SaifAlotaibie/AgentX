"""
Language detection and intent extraction utilities.
Supports both English and Arabic.
"""

import re
from typing import Optional

def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    
    Args:
        text: Input text
        
    Returns:
        'ar' for Arabic, 'en' for English
    """
    # Check for Arabic characters (Unicode range U+0600 to U+06FF)
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    
    if arabic_pattern.search(text):
        return "ar"
    return "en"

def extract_intent(message: str, language: Optional[str] = None) -> str:
    """
    Extract user intent from the message using keyword matching.
    
    Args:
        message: User message
        language: Language code ('ar' or 'en'), will auto-detect if not provided
        
    Returns:
        Intent string: 'resume_add', 'resume_edit', 'resume_delete', or 'qa'
    """
    if language is None:
        language = detect_language(message)
    
    message_lower = message.lower()
    
    # Arabic keywords for resume operations
    arabic_resume_keywords = ["سيرة", "سيرتي", "cv", "resume"]
    arabic_add_keywords = ["إضافة", "إضافه", "إنشاء", "انشاء", "أضف", "اضف", "جديد", "جديدة"]
    arabic_edit_keywords = ["تعديل", "تحديث", "تغيير", "عدل", "حدث", "غير"]
    arabic_delete_keywords = ["حذف", "إزالة", "ازالة", "احذف", "أزل", "ازل", "مسح"]
    
    # English keywords for resume operations
    english_resume_keywords = ["resume", "cv", "curriculum vitae"]
    english_add_keywords = ["add", "create", "new", "make", "build"]
    english_edit_keywords = ["edit", "update", "modify", "change", "revise"]
    english_delete_keywords = ["delete", "remove", "erase"]
    
    # Check for resume-related intents
    has_resume_keyword = False
    
    if language == "ar":
        has_resume_keyword = any(keyword in message_lower for keyword in arabic_resume_keywords)
        
        if has_resume_keyword or any(keyword in message_lower for keyword in arabic_add_keywords):
            if any(keyword in message_lower for keyword in arabic_add_keywords):
                return "resume_add"
        
        if has_resume_keyword or any(keyword in message_lower for keyword in arabic_edit_keywords):
            if any(keyword in message_lower for keyword in arabic_edit_keywords):
                return "resume_edit"
        
        if has_resume_keyword or any(keyword in message_lower for keyword in arabic_delete_keywords):
            if any(keyword in message_lower for keyword in arabic_delete_keywords):
                return "resume_delete"
    
    else:  # English
        has_resume_keyword = any(keyword in message_lower for keyword in english_resume_keywords)
        
        if has_resume_keyword or any(keyword in message_lower for keyword in english_add_keywords):
            if any(keyword in message_lower for keyword in english_add_keywords):
                return "resume_add"
        
        if has_resume_keyword or any(keyword in message_lower for keyword in english_edit_keywords):
            if any(keyword in message_lower for keyword in english_edit_keywords):
                return "resume_edit"
        
        if has_resume_keyword or any(keyword in message_lower for keyword in english_delete_keywords):
            if any(keyword in message_lower for keyword in english_delete_keywords):
                return "resume_delete"
    
    # If no resume intent detected, classify as Q&A
    return "qa"

def is_confirmation(message: str, language: Optional[str] = None) -> bool:
    """
    Check if the message is a confirmation (yes/no).
    
    Args:
        message: User message
        language: Language code ('ar' or 'en'), will auto-detect if not provided
        
    Returns:
        True if message is a confirmation (yes), False otherwise
    """
    if language is None:
        language = detect_language(message)
    
    message_lower = message.lower().strip()
    
    if language == "ar":
        yes_keywords = ["نعم", "أجل", "اجل", "موافق", "تمام", "صحيح", "حسنا", "ok", "yes"]
        no_keywords = ["لا", "كلا", "لأ", "غير موافق", "no"]
    else:
        yes_keywords = ["yes", "yeah", "yep", "sure", "ok", "okay", "confirm", "agreed"]
        no_keywords = ["no", "nope", "nah", "cancel", "disagree"]
    
    if any(keyword in message_lower for keyword in yes_keywords):
        return True
    
    return False

