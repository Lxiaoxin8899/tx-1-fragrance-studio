#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据导入导出工具
"""

import json
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DataImportExport:
    """数据导入导出工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def export_recipe_to_json(self, recipe_data: Dict[str, Any], 
                             file_path: str, 
                             include_version_history: bool = True) -> bool:
        """导出配方到JSON文件"""
        try:
            export_data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'tool_version': '2.0.0',
                    'format_version': '1.0'
                },
                'recipe': recipe_data
            }
            
            if not include_version_history:
                export_data['recipe'].pop('version_history', None)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"配方已导出到: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出配方失败: {e}")
            return False
    
    def import_recipe_from_json(self, file_path: str) -> Optional[Dict[str, Any]]:
        """从JSON文件导入配方"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证数据格式
            if 'recipe' not in data:
                raise ValueError("无效的配方文件格式")
            
            recipe_data = data['recipe']
            
            # 基本验证
            required_fields = ['name', 'version', 'compositions']
            for field in required_fields:
                if field not in recipe_data:
                    raise ValueError(f"缺少必要字段: {field}")
            
            self.logger.info(f"成功导入配方: {recipe_data['name']}")
            return recipe_data
            
        except Exception as e:
            self.logger.error(f"导入配方失败: {e}")
            return None
    
    def export_recipes_to_excel(self, recipes_data: List[Dict[str, Any]], 
                               file_path: str) -> bool:
        """导出多个配方到Excel文件"""
        try:
            # 准备数据
            recipe_rows = []
            composition_rows = []
            
            for recipe in recipes_data:
                # 配方基本信息
                recipe_rows.append({
                    '配方ID': recipe.get('id'),
                    '配方名称': recipe.get('name'),
                    '版本': recipe.get('version', 1),
                    '总容量(ml)': recipe.get('total_volume_ml', 0.0),
                    '尼古丁浓度(mg)': recipe.get('nicotine_strength_mg', 0.0),
                    'PG比例(%)': recipe.get('pg_ratio', 0.0),
                    'VG比例(%)': recipe.get('vg_ratio', 0.0),
                    '香精比例(%)': recipe.get('flavor_ratio', 0.0),
                    '设计师': recipe.get('designer_name'),
                    '客户': recipe.get('customer_name'),
                    '创建时间': recipe.get('created_at'),
                    '更新时间': recipe.get('updated_at')
                })
                
                # 配方组成
                for comp in recipe.get('compositions', []):
                    composition_rows.append({
                        '配方ID': recipe.get('id'),
                        '配方名称': recipe.get('name'),
                        '材料ID': comp.get('material_id'),
                        '材料名称': comp.get('material_name', ''),
                        '百分比(%)': comp.get('percentage', 0.0),
                        '重量(g)': comp.get('weight_grams', 0.0)
                    })
            
            # 创建Excel文件
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                if recipe_rows:
                    pd.DataFrame(recipe_rows).to_excel(writer, sheet_name='配方列表', index=False)
                if composition_rows:
                    pd.DataFrame(composition_rows).to_excel(writer, sheet_name='配方组成', index=False)
            
            self.logger.info(f"配方已导出到Excel: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出到Excel失败: {e}")
            return False
    
    def export_analysis_report(self, recipe_data: Dict[str, Any], 
                              analysis_result: Dict[str, Any], 
                              file_path: str) -> bool:
        """导出分析报告"""
        try:
            report_data = {
                'recipe_info': {
                    'name': recipe_data.get('name'),
                    'version': recipe_data.get('version', 1),
                    'total_volume_ml': recipe_data.get('total_volume_ml', 0.0),
                    'designer': recipe_data.get('designer_name'),
                    'customer': recipe_data.get('customer_name')
                },
                'analysis_results': analysis_result,
                'export_date': datetime.now().isoformat()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"分析报告已导出: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出分析报告失败: {e}")
            return False
    
    def validate_recipe_data(self, recipe_data: Dict[str, Any]) -> List[str]:
        """验证配方数据"""
        errors = []
        
        # 检查必要字段
        required_fields = ['name', 'version', 'compositions']
        for field in required_fields:
            if field not in recipe_data:
                errors.append(f"缺少必要字段: {field}")
        
        # 检查配方组成
        compositions = recipe_data.get('compositions', [])
        total_percentage = sum(comp.get('percentage', 0.0) for comp in compositions)
        
        if abs(total_percentage - 100.0) > 0.1:
            errors.append(f"配方总百分比异常: {total_percentage:.2f}% (应为100%)")
        
        # 检查单个材料比例
        for i, comp in enumerate(compositions):
            percentage = comp.get('percentage', 0.0)
            if percentage <= 0.0:
                errors.append(f"材料 {i+1}: 比例必须大于0")
            if percentage > 30.0:
                errors.append(f"材料 {comp.get('material_name', '未知')}: 比例过高 ({percentage:.2f}%)")
        
        return errors