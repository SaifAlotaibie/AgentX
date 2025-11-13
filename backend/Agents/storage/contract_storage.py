"""
Contract storage system using DUAL STORAGE: JSON files + Supabase.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from config.settings import LOG_PATH

# Create contracts directory
CONTRACTS_PATH = LOG_PATH / "contracts"
CONTRACTS_PATH.mkdir(parents=True, exist_ok=True)

# Import Supabase storage
try:
    from database.supabase_storage import supabase_contract_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase not available for contracts: {e}")
    SUPABASE_AVAILABLE = False


class ContractStorage:
    """Manages contract storage in JSON files + Supabase."""
    
    def __init__(self):
        """Initialize storage."""
        CONTRACTS_PATH.mkdir(parents=True, exist_ok=True)
    
    def _get_user_file(self, userId: str) -> Path:
        """Get the JSON file path for a user's contracts."""
        return CONTRACTS_PATH / f"{userId}_contracts.json"
    
    def _load_user_contracts(self, userId: str) -> List[Dict[str, Any]]:
        """Load all contracts for a user."""
        file_path = self._get_user_file(userId)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_user_contracts(self, userId: str, contracts: List[Dict[str, Any]]):
        """Save all contracts for a user."""
        file_path = self._get_user_file(userId)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(contracts, f, ensure_ascii=False, indent=2)
    
    def save_contract(self, userId: str, contractId: str, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a contract to JSON (primary) and Supabase (secondary).
        """
        contracts = self._load_user_contracts(userId)
        
        # Create contract object
        contract = {
            "contractId": contractId,
            "userId": userId,
            "data": contract_data,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }
        
        # PRIMARY: Save to JSON
        contracts.append(contract)
        self._save_user_contracts(userId, contracts)
        
        # SECONDARY: Save to Supabase
        if SUPABASE_AVAILABLE:
            try:
                supabase_contract_storage.save_contract(userId, contractId, contract_data)
            except Exception as e:
                print(f"⚠️ Supabase save failed (non-critical): {e}")
        
        return contract
    
    def get_contract(self, userId: str, contractId: str) -> Optional[Dict[str, Any]]:
        """Get a specific contract."""
        contracts = self._load_user_contracts(userId)
        
        for contract in contracts:
            if contract["contractId"] == contractId:
                return contract
        
        return None
    
    def get_all_contracts(self, userId: str) -> List[Dict[str, Any]]:
        """Get all contracts for a user."""
        return self._load_user_contracts(userId)
    
    def update_contract(self, userId: str, contractId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a contract."""
        contracts = self._load_user_contracts(userId)
        
        for i, contract in enumerate(contracts):
            if contract["contractId"] == contractId:
                # Update data
                contract["data"].update(changes)
                contract["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                contracts[i] = contract
                
                # PRIMARY: Save to JSON
                self._save_user_contracts(userId, contracts)
                
                # SECONDARY: Update in Supabase
                if SUPABASE_AVAILABLE:
                    try:
                        supabase_contract_storage.update_contract(userId, contractId, changes)
                    except Exception as e:
                        print(f"⚠️ Supabase update failed (non-critical): {e}")
                
                return contract
        
        return None
    
    def delete_contract(self, userId: str, contractId: str) -> bool:
        """Delete a contract."""
        contracts = self._load_user_contracts(userId)
        original_count = len(contracts)
        
        contracts = [c for c in contracts if c["contractId"] != contractId]
        
        if len(contracts) < original_count:
            # PRIMARY: Delete from JSON
            self._save_user_contracts(userId, contracts)
            
            # SECONDARY: Delete from Supabase
            if SUPABASE_AVAILABLE:
                try:
                    supabase_contract_storage.delete_contract(userId, contractId)
                except Exception as e:
                    print(f"⚠️ Supabase delete failed (non-critical): {e}")
            
            return True
        
        return False


# Singleton instance
contract_storage = ContractStorage()

