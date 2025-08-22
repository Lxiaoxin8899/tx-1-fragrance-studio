#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配方分析服务 - 提供配方智能分析功能
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class FlavorCategory(Enum):
    """香调分类枚举"""
    TOP = "top"      # 前调
    MIDDLE = "middle" # 中调
    BASE = "base"    # 后调
    OTHER = "other"  # 其他


@dataclass
class AnalysisResult:
    """分析结果数据类"""
    flavor_balance: Dict[str, float]  # 香调平衡度
    persistence_score: float         # 持久性评分
    cost_analysis: Dict[str, Any]    # 成本分析
    recommendations: List[str]       # 优化建议
    warnings: List[str]              # 警告信息


class RecipeAnalyzer:
    """配方分析器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 香调分类映射
        self.flavor_categories = {
            'citrus': FlavorCategory.TOP,
            'fruit': FlavorCategory.TOP,
            'berry': FlavorCategory.TOP,
            'mint': FlavorCategory.TOP,
            'floral': FlavorCategory.MIDDLE,
            'spice': FlavorCategory.MIDDLE,
            'nut': FlavorCategory.MIDDLE,
            'cream': FlavorCategory.MIDDLE,
            'tobacco': FlavorCategory.BASE,
            'vanilla': FlavorCategory.BASE,
            'caramel': FlavorCategory.BASE,
            'chocolate': FlavorCategory.BASE
        }
    
    def analyze_recipe(self, recipe_data: Dict[str, Any]) -> AnalysisResult:
        """分析配方"""
        try:
            # 香调平衡分析
            flavor_balance = self._analyze_flavor_balance(recipe_data)
            
            # 持久性分析
            persistence_score = self._analyze_persistence(recipe_data)
            
            # 成本分析
            cost_analysis = self._analyze_cost(recipe_data)
            
            # 生成建议和警告
            recommendations = self._generate_recommendations(flavor_balance, persistence_score)
            warnings = self._generate_warnings(recipe_data)
            
            return AnalysisResult(
                flavor_balance=flavor_balance,
                persistence_score=persistence_score,
                cost_analysis=cost_analysis,
                recommendations=recommendations,
                warnings=warnings
            )
            
        except Exception as e:
            self.logger.error(f"配方分析错误: {e}")
            raise
    
    def _analyze_flavor_balance(self, recipe_data: Dict[str, Any]) -> Dict[str, float]:
        """分析香调平衡"""
        category_totals = {
            FlavorCategory.TOP.value: 0.0,
            FlavorCategory.MIDDLE.value: 0.0,
            FlavorCategory.BASE.value: 0.0,
            FlavorCategory.OTHER.value: 0.0
        }
        
        compositions = recipe_data.get('compositions', [])
        for comp in compositions:
            material_name = comp.get('material_name', '').lower()
            percentage = comp.get('percentage', 0.0)
            
            # 确定香调分类
            category = FlavorCategory.OTHER
            for keyword, cat in self.flavor_categories.items():
                if keyword in material_name:
                    category = cat
                    break
            
            category_totals[category.value] += percentage
        
        # 计算比例
        total_percentage = sum(category_totals.values())
        if total_percentage > 0:
            for category in category_totals:
                category_totals[category] = (category_totals[category] / total_percentage) * 100
        
        return category_totals
    
    def _analyze_persistence(self, recipe_data: Dict[str, Any]) -> float:
        """分析持久性"""
        base_percentage = 0.0
        top_percentage = 0.0
        
        compositions = recipe_data.get('compositions', [])
        for comp in compositions:
            material_name = comp.get('material_name', '').lower()
            percentage = comp.get('percentage', 0.0)
            
            # 后调材料增加持久性
            if any(keyword in material_name for keyword in ['tobacco', 'vanilla', 'caramel', 'chocolate']):
                base_percentage += percentage
            # 前调材料降低持久性
            elif any(keyword in material_name for keyword in ['citrus', 'mint']):
                top_percentage += percentage
        
        # 计算持久性评分 (0-10)
        persistence_score = min(10.0, (base_percentage - top_percentage * 0.5) / 10.0 + 5.0)
        return max(0.0, min(10.0, persistence_score))
    
    def _analyze_cost(self, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """成本分析"""
        total_cost = 0.0
        material_costs = []
        
        compositions = recipe_data.get('compositions', [])
        total_volume = recipe_data.get('total_volume_ml', 30.0)
        
        for comp in compositions:
            material_price = comp.get('price_per_ml', 0.0)
            percentage = comp.get('percentage', 0.0)
            
            # 计算材料成本
            volume_ml = total_volume * percentage / 100.0
            cost = volume_ml * material_price
            total_cost += cost
            
            material_costs.append({
                'material_name': comp.get('material_name', ''),
                'percentage': percentage,
                'cost': cost,
                'cost_percentage': (cost / total_cost * 100) if total_cost > 0 else 0.0
            })
        
        return {
            'total_cost': total_cost,
            'cost_per_ml': total_cost / total_volume if total_volume > 0 else 0.0,
            'material_costs': material_costs,
            'total_volume_ml': total_volume
        }
    
    def _generate_recommendations(self, flavor_balance: Dict[str, float], 
                                 persistence_score: float) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 香调平衡建议
        top = flavor_balance.get(FlavorCategory.TOP.value, 0.0)
        middle = flavor_balance.get(FlavorCategory.MIDDLE.value, 0.0)
        base = flavor_balance.get(FlavorCategory.BASE.value, 0.0)
        
        if top > 40:
            recommendations.append("前调比例过高，建议增加中后调材料平衡香气")
        if middle < 20:
            recommendations.append("中调比例不足，建议增加 floral、spice 类材料")
        if base < 15:
            recommendations.append("后调比例不足，建议增加 tobacco、vanilla 类材料增强持久性")
        
        # 持久性建议
        if persistence_score < 5.0:
            recommendations.append("持久性较低，建议增加后调材料比例")
        elif persistence_score > 8.0:
            recommendations.append("持久性优秀，但可能影响前调表现")
        
        return recommendations
    
    def _generate_warnings(self, recipe_data: Dict[str, Any]) -> List[str]:
        """生成警告信息"""
        warnings = []
        compositions = recipe_data.get('compositions', [])
        
        # 检查总百分比
        total_percentage = sum(comp.get('percentage', 0.0) for comp in compositions)
        if abs(total_percentage - 100.0) > 0.1:
            warnings.append(f"配方总百分比异常: {total_percentage:.2f}% (应为100%)")
        
        # 检查单个材料比例
        for comp in compositions:
            percentage = comp.get('percentage', 0.0)
            if percentage > 20.0:
                warnings.append(f"材料 {comp.get('material_name', '')} 比例过高: {percentage:.2f}%")
            if percentage < 0.1:
                warnings.append(f"材料 {comp.get('material_name', '')} 比例过低: {percentage:.2f}%")
        
        return warnings