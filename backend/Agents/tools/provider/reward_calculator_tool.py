"""
End of service reward calculator tool for service providers.
"""

from datetime import datetime
from typing import Dict, Any
from utils.logger import log_action, log_error


class RewardCalculatorTool:
    """Tool for calculating end of service rewards based on Saudi labor law."""
    
    def __init__(self):
        """Initialize the RewardCalculatorTool."""
        pass
    
    def calculate_reward(
        self,
        userId: str,
        start_date: str,
        end_date: str,
        monthly_salary: float,
        termination_type: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Calculate end of service reward.
        
        Args:
            userId: User ID (service provider)
            start_date: Employment start date (ISO format)
            end_date: Employment end date (ISO format)
            monthly_salary: Monthly salary in SAR
            termination_type: "resignation", "contract_end", or "termination"
            sessionId: Session ID for logging
            
        Returns:
            Dictionary with calculation result and explanation
        """
        try:
            # Parse dates
            start = datetime.fromisoformat(start_date.replace('Z', ''))
            end = datetime.fromisoformat(end_date.replace('Z', ''))
            
            # Calculate years and months
            total_days = (end - start).days
            total_years = total_days / 365.25
            full_years = int(total_years)
            remaining_months = int((total_years - full_years) * 12)
            
            # Calculate reward based on Saudi labor law
            reward = 0
            explanation = []
            
            if termination_type == "resignation" and total_years < 2:
                # No reward if resigned before 2 years
                reward = 0
                explanation.append("لا يستحق مكافأة (استقالة قبل سنتين)")
            
            elif termination_type == "resignation" and 2 <= total_years < 5:
                # 1/3 of reward for resignation between 2-5 years
                base_reward = self._calculate_base_reward(full_years, remaining_months, monthly_salary)
                reward = base_reward / 3
                explanation.append(f"استقالة بعد {full_years} سنة: ثلث المكافأة")
                explanation.append(f"المكافأة الأساسية: {base_reward:,.2f} ريال")
                explanation.append(f"ثلث المكافأة: {reward:,.2f} ريال")
            
            elif termination_type == "resignation" and 5 <= total_years < 10:
                # 2/3 of reward for resignation between 5-10 years
                base_reward = self._calculate_base_reward(full_years, remaining_months, monthly_salary)
                reward = (base_reward * 2) / 3
                explanation.append(f"استقالة بعد {full_years} سنة: ثلثي المكافأة")
                explanation.append(f"المكافأة الأساسية: {base_reward:,.2f} ريال")
                explanation.append(f"ثلثي المكافأة: {reward:,.2f} ريال")
            
            else:
                # Full reward for 10+ years or contract end or termination
                reward = self._calculate_base_reward(full_years, remaining_months, monthly_salary)
                if termination_type == "contract_end":
                    explanation.append("انتهاء عقد: مكافأة كاملة")
                elif termination_type == "termination":
                    explanation.append("فصل من العمل: مكافأة كاملة")
                else:
                    explanation.append(f"استقالة بعد {full_years} سنة: مكافأة كاملة")
            
            # Add calculation breakdown
            explanation.append(f"\nمدة الخدمة: {full_years} سنة و {remaining_months} شهر")
            explanation.append(f"الراتب الشهري: {monthly_salary:,.2f} ريال")
            
            result = {
                "status": "success",
                "reward_amount": round(reward, 2),
                "currency": "SAR",
                "years_of_service": full_years,
                "months_of_service": remaining_months,
                "termination_type": termination_type,
                "explanation": "\n".join(explanation),
                "message": f"مكافأة نهاية الخدمة: {reward:,.2f} ريال سعودي"
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="service_provider",
                tool="RewardCalculatorTool.calculate_reward",
                inputs={
                    "userId": userId,
                    "start_date": start_date,
                    "end_date": end_date,
                    "monthly_salary": monthly_salary,
                    "termination_type": termination_type
                },
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="service_provider",
                tool="RewardCalculatorTool.calculate_reward",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def _calculate_base_reward(self, full_years: int, remaining_months: int, monthly_salary: float) -> float:
        """
        Calculate base reward according to Saudi labor law.
        - First 5 years: half month salary per year
        - After 5 years: full month salary per year
        """
        reward = 0
        
        # First 5 years: 0.5 month per year
        years_first_period = min(full_years, 5)
        reward += years_first_period * (monthly_salary / 2)
        
        # After 5 years: 1 month per year
        if full_years > 5:
            years_second_period = full_years - 5
            reward += years_second_period * monthly_salary
        
        # Add proportional reward for remaining months
        if remaining_months > 0:
            if full_years < 5:
                reward += remaining_months * (monthly_salary / 24)  # 0.5 month / 12 months
            else:
                reward += remaining_months * (monthly_salary / 12)  # 1 month / 12 months
        
        return reward

