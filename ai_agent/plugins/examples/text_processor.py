"""
Example text processing plugin
"""

from typing import List, Dict, Any
from ..base import BasePlugin, PluginResult
import re
import string


class TextProcessingPlugin(BasePlugin):
    """Text processing plugin for various text operations"""
    
    def __init__(self):
        super().__init__(
            name="text_processor",
            description="Performs various text processing operations",
            version="1.0.0"
        )
    
    async def execute(self, operation: str, text: str, **kwargs) -> PluginResult:
        """Execute a text processing operation"""
        try:
            if operation == "word_count":
                result = self._word_count(text)
            elif operation == "char_count":
                result = self._char_count(text)
            elif operation == "line_count":
                result = self._line_count(text)
            elif operation == "uppercase":
                result = text.upper()
            elif operation == "lowercase":
                result = text.lower()
            elif operation == "title_case":
                result = text.title()
            elif operation == "reverse":
                result = text[::-1]
            elif operation == "remove_punctuation":
                result = self._remove_punctuation(text)
            elif operation == "extract_emails":
                result = self._extract_emails(text)
            elif operation == "extract_urls":
                result = self._extract_urls(text)
            elif operation == "summarize":
                result = self._simple_summarize(text, kwargs.get("max_sentences", 3))
            else:
                return PluginResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            return PluginResult(
                success=True,
                data=result,
                metadata={"operation": operation, "text_length": len(text)}
            )
            
        except Exception as e:
            return PluginResult(
                success=False,
                error=f"Text processing error: {str(e)}",
                metadata={"operation": operation}
            )
    
    def _word_count(self, text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    def _char_count(self, text: str) -> Dict[str, int]:
        """Count characters in text"""
        return {
            "total": len(text),
            "excluding_spaces": len(text.replace(" ", "")),
            "letters": sum(1 for c in text if c.isalpha()),
            "digits": sum(1 for c in text if c.isdigit()),
            "punctuation": sum(1 for c in text if c in string.punctuation),
        }
    
    def _line_count(self, text: str) -> int:
        """Count lines in text"""
        return len(text.splitlines())
    
    def _remove_punctuation(self, text: str) -> str:
        """Remove punctuation from text"""
        return text.translate(str.maketrans("", "", string.punctuation))
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def _simple_summarize(self, text: str, max_sentences: int = 3) -> str:
        """Simple text summarization by selecting first N sentences"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        return '. '.join(sentences[:max_sentences]) + '.'
    
    def get_capabilities(self) -> List[str]:
        """Get text processing capabilities"""
        return [
            "word_count",
            "char_count",
            "line_count",
            "case_conversion",
            "text_reversal",
            "punctuation_removal",
            "email_extraction",
            "url_extraction",
            "simple_summarization",
        ]
    
    def validate_input(self, operation: str, text: str, **kwargs) -> bool:
        """Validate input parameters"""
        if not isinstance(operation, str) or not isinstance(text, str):
            return False
        
        valid_operations = [
            "word_count", "char_count", "line_count", "uppercase", "lowercase",
            "title_case", "reverse", "remove_punctuation", "extract_emails",
            "extract_urls", "summarize"
        ]
        
        return operation in valid_operations
    
    async def setup(self) -> None:
        """Setup the text processing plugin"""
        # No special setup needed
        pass
    
    async def cleanup(self) -> None:
        """Cleanup the text processing plugin"""
        # No cleanup needed
        pass
