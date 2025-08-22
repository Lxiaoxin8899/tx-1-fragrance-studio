#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配方数据模型
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class VersionType(Enum):
    """版本类型枚举"""
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


class ChangeType(Enum):
    """变更类型枚举"""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    COPIED = "copied"
    IMPORTED = "imported"


@dataclass
class Material:
    """材料数据类"""
    id: int
    name: str
    category: str
    description: Optional[str] = None
    price_per_ml: float = 0.0
    density: float = 1.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class RecipeComposition:
    """配方组成数据类"""
    id: int
    recipe_id: int
    material_id: int
    percentage: float
    weight_grams: float = 0.0
    created_at: Optional[datetime] = None
    material: Optional[Material] = None


@dataclass
class VersionHistory:
    """版本历史数据类"""
    id: int
    recipe_id: int
    version: int
    change_type: ChangeType
    change_description: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Recipe:
    """配方数据类"""
    id: int
    name: str
    version: int = 1
    parent_recipe_id: Optional[int] = None
    description: Optional[str] = None
    total_volume_ml: float = 0.0
    nicotine_strength_mg: float = 0.0
    pg_ratio: float = 0.0
    vg_ratio: float = 0.0
    flavor_ratio: float = 0.0
    designer_name: Optional[str] = None
    customer_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # 关联数据
    compositions: List[RecipeComposition] = field(default_factory=list)
    version_history: List[VersionHistory] = field(default_factory=list)
    child_recipes: List['Recipe'] = field(default_factory=list)
    
    def calculate_totals(self) -> Dict[str, float]:
        """计算配方统计信息"""
        total_percentage = sum(comp.percentage for comp in self.compositions)
        total_weight = sum(comp.weight_grams for comp in self.compositions)
        
        # 按分类统计
        category_stats = {}
        for comp in self.compositions:
            if comp.material:
                category = comp.material.category
                if category not in category_stats:
                    category_stats[category] = 0.0
                category_stats[category] += comp.percentage
        
        return {
            'total_percentage': total_percentage,
            'total_weight': total_weight,
            'category_stats': category_stats,
            'material_count': len(self.compositions)
        }
    
    def validate_composition(self) -> bool:
        """验证配方组成是否有效"""
        total_percentage = sum(comp.percentage for comp in self.compositions)
        return abs(total_percentage - 100.0) < 0.01  # 允许微小误差
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'parent_recipe_id': self.parent_recipe_id,
            'description': self.description,
            'total_volume_ml': self.total_volume_ml,
            'nicotine_strength_mg': self.nicotine_strength_mg,
            'pg_ratio': self.pg_ratio,
            'vg_ratio': self.vg_ratio,
            'flavor_ratio': self.flavor_ratio,
            'designer_name': self.designer_name,
            'customer_name': self.customer_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'compositions': [
                {
                    'id': comp.id,
                    'material_id': comp.material_id,
                    'percentage': comp.percentage,
                    'weight_grams': comp.weight_grams
                } for comp in self.compositions
            ],
            'version_history': [
                {
                    'id': hist.id,
                    'version': hist.version,
                    'change_type': hist.change_type.value,
                    'change_description': hist.change_description,
                    'created_by': hist.created_by,
                    'created_at': hist.created_at.isoformat() if hist.created_at else None
                } for hist in self.version_history
            ]
        }