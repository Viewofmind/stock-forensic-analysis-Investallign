"""
Forensic analysis module for calculating financial fraud indicators
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

from src.utils import safe_divide, calculate_percentage_change


class ForensicAnalyzer:
    """Perform forensic analysis on financial data"""
    
    def __init__(self, financial_data: Dict[str, Any]):
        """
        Initialize the forensic analyzer
        
        Args:
            financial_data: Dictionary containing financial statements and ratios
        """
        self.financial_data = financial_data
        self.balance_sheet = financial_data.get('financials', {}).get('balance_sheet', pd.DataFrame())
        self.income_statement = financial_data.get('financials', {}).get('income_statement', pd.DataFrame())
        self.cash_flow = financial_data.get('financials', {}).get('cash_flow', pd.DataFrame())
        self.stock_info = financial_data.get('stock_info', {})
    
    def calculate_beneish_m_score(self) -> Dict[str, Any]:
        """
        Calculate Beneish M-Score for earnings manipulation detection
        
        The M-Score uses 8 variables:
        1. DSRI (Days Sales in Receivables Index)
        2. GMI (Gross Margin Index)
        3. AQI (Asset Quality Index)
        4. SGI (Sales Growth Index)
        5. DEPI (Depreciation Index)
        6. SGAI (Sales, General and Administrative Expenses Index)
        7. LVGI (Leverage Index)
        8. TATA (Total Accruals to Total Assets)
        
        M-Score > -2.22 suggests possible manipulation
        
        Returns:
            Dictionary with M-Score and component variables
        """
        try:
            result = {
                'score': None,
                'interpretation': '',
                'risk_level': 'UNKNOWN',
                'components': {},
                'calculation_possible': False
            }
            
            # Check if we have enough data
            if self.balance_sheet.empty or self.income_statement.empty:
                result['interpretation'] = 'Insufficient financial data for M-Score calculation'
                return result
            
            # Get current and previous year data
            if len(self.balance_sheet.columns) < 2 or len(self.income_statement.columns) < 2:
                result['interpretation'] = 'Need at least 2 years of data for M-Score calculation'
                return result
            
            # Extract financial metrics (current year = index 0, previous year = index 1)
            try:
                # Receivables
                receivables_current = self._get_value(self.balance_sheet, 'Accounts Receivable', 0)
                receivables_previous = self._get_value(self.balance_sheet, 'Accounts Receivable', 1)
                
                # Revenue
                revenue_current = self._get_value(self.income_statement, 'Total Revenue', 0)
                revenue_previous = self._get_value(self.income_statement, 'Total Revenue', 1)
                
                # Cost of Revenue
                cogs_current = self._get_value(self.income_statement, 'Cost Of Revenue', 0)
                cogs_previous = self._get_value(self.income_statement, 'Cost Of Revenue', 1)
                
                # Total Assets
                assets_current = self._get_value(self.balance_sheet, 'Total Assets', 0)
                assets_previous = self._get_value(self.balance_sheet, 'Total Assets', 1)
                
                # Current Assets
                current_assets_current = self._get_value(self.balance_sheet, 'Total Current Assets', 0)
                current_assets_previous = self._get_value(self.balance_sheet, 'Total Current Assets', 1)
                
                # PPE (Property, Plant, Equipment)
                ppe_current = self._get_value(self.balance_sheet, 'Net PPE', 0)
                ppe_previous = self._get_value(self.balance_sheet, 'Net PPE', 1)
                
                # Depreciation
                depreciation_current = abs(self._get_value(self.cash_flow, 'Depreciation', 0))
                depreciation_previous = abs(self._get_value(self.cash_flow, 'Depreciation', 1))
                
                # SG&A Expenses
                sga_current = self._get_value(self.income_statement, 'Selling General And Administration', 0)
                sga_previous = self._get_value(self.income_statement, 'Selling General And Administration', 1)
                
                # Total Liabilities
                liabilities_current = self._get_value(self.balance_sheet, 'Total Liabilities Net Minority Interest', 0)
                liabilities_previous = self._get_value(self.balance_sheet, 'Total Liabilities Net Minority Interest', 1)
                
                # Net Income
                net_income = self._get_value(self.income_statement, 'Net Income', 0)
                
                # Operating Cash Flow
                operating_cf = self._get_value(self.cash_flow, 'Operating Cash Flow', 0)
                
                # Calculate the 8 variables
                
                # 1. DSRI (Days Sales in Receivables Index)
                receivables_to_sales_current = safe_divide(receivables_current, revenue_current)
                receivables_to_sales_previous = safe_divide(receivables_previous, revenue_previous)
                dsri = safe_divide(receivables_to_sales_current, receivables_to_sales_previous, 1.0)
                
                # 2. GMI (Gross Margin Index)
                gross_margin_previous = safe_divide(revenue_previous - cogs_previous, revenue_previous)
                gross_margin_current = safe_divide(revenue_current - cogs_current, revenue_current)
                gmi = safe_divide(gross_margin_previous, gross_margin_current, 1.0)
                
                # 3. AQI (Asset Quality Index)
                non_current_assets_current = assets_current - current_assets_current - ppe_current
                non_current_assets_previous = assets_previous - current_assets_previous - ppe_previous
                aqi_current = safe_divide(non_current_assets_current, assets_current)
                aqi_previous = safe_divide(non_current_assets_previous, assets_previous)
                aqi = safe_divide(aqi_current, aqi_previous, 1.0)
                
                # 4. SGI (Sales Growth Index)
                sgi = safe_divide(revenue_current, revenue_previous, 1.0)
                
                # 5. DEPI (Depreciation Index)
                depr_rate_previous = safe_divide(depreciation_previous, depreciation_previous + ppe_previous)
                depr_rate_current = safe_divide(depreciation_current, depreciation_current + ppe_current)
                depi = safe_divide(depr_rate_previous, depr_rate_current, 1.0)
                
                # 6. SGAI (SG&A Index)
                sga_to_sales_current = safe_divide(sga_current, revenue_current)
                sga_to_sales_previous = safe_divide(sga_previous, revenue_previous)
                sgai = safe_divide(sga_to_sales_current, sga_to_sales_previous, 1.0)
                
                # 7. LVGI (Leverage Index)
                leverage_current = safe_divide(liabilities_current, assets_current)
                leverage_previous = safe_divide(liabilities_previous, assets_previous)
                lvgi = safe_divide(leverage_current, leverage_previous, 1.0)
                
                # 8. TATA (Total Accruals to Total Assets)
                total_accruals = net_income - operating_cf
                tata = safe_divide(total_accruals, assets_current)
                
                # Calculate M-Score using Beneish's formula
                m_score = (
                    -4.84 +
                    0.920 * dsri +
                    0.528 * gmi +
                    0.404 * aqi +
                    0.892 * sgi +
                    0.115 * depi -
                    0.172 * sgai +
                    4.679 * tata -
                    0.327 * lvgi
                )
                
                result['score'] = round(m_score, 3)
                result['calculation_possible'] = True
                result['components'] = {
                    'DSRI': round(dsri, 3),
                    'GMI': round(gmi, 3),
                    'AQI': round(aqi, 3),
                    'SGI': round(sgi, 3),
                    'DEPI': round(depi, 3),
                    'SGAI': round(sgai, 3),
                    'LVGI': round(lvgi, 3),
                    'TATA': round(tata, 3)
                }
                
                # Interpret the score
                if m_score > -2.22:
                    result['risk_level'] = 'HIGH'
                    result['interpretation'] = 'M-Score suggests possible earnings manipulation. Score > -2.22 indicates higher likelihood of manipulation.'
                else:
                    result['risk_level'] = 'LOW'
                    result['interpretation'] = 'M-Score suggests lower likelihood of earnings manipulation. Score <= -2.22 indicates company is likely not manipulating earnings.'
                
            except Exception as e:
                result['interpretation'] = f'Error calculating M-Score components: {str(e)}'
            
            return result
            
        except Exception as e:
            return {
                'score': None,
                'interpretation': f'Error calculating M-Score: {str(e)}',
                'risk_level': 'UNKNOWN',
                'components': {},
                'calculation_possible': False
            }
    
    def calculate_altman_z_score(self) -> Dict[str, Any]:
        """
        Calculate Altman Z-Score for bankruptcy prediction
        
        Z-Score uses 5 ratios:
        1. Working Capital / Total Assets
        2. Retained Earnings / Total Assets
        3. EBIT / Total Assets
        4. Market Value of Equity / Total Liabilities
        5. Sales / Total Assets
        
        Z > 2.99 = Safe Zone
        1.81 < Z < 2.99 = Grey Zone
        Z < 1.81 = Distress Zone
        
        Returns:
            Dictionary with Z-Score and interpretation
        """
        try:
            result = {
                'score': None,
                'interpretation': '',
                'risk_level': 'UNKNOWN',
                'components': {},
                'calculation_possible': False
            }
            
            if self.balance_sheet.empty or self.income_statement.empty:
                result['interpretation'] = 'Insufficient financial data for Z-Score calculation'
                return result
            
            # Extract financial metrics
            try:
                # Balance Sheet items
                current_assets = self._get_value(self.balance_sheet, 'Total Current Assets', 0)
                current_liabilities = self._get_value(self.balance_sheet, 'Total Current Liabilities', 0)
                total_assets = self._get_value(self.balance_sheet, 'Total Assets', 0)
                total_liabilities = self._get_value(self.balance_sheet, 'Total Liabilities Net Minority Interest', 0)
                retained_earnings = self._get_value(self.balance_sheet, 'Retained Earnings', 0)
                
                # Income Statement items
                ebit = self._get_value(self.income_statement, 'EBIT', 0)
                revenue = self._get_value(self.income_statement, 'Total Revenue', 0)
                
                # Market data
                market_cap = self.stock_info.get('market_cap', 0)
                
                # Calculate working capital
                working_capital = current_assets - current_liabilities
                
                # Calculate the 5 ratios
                x1 = safe_divide(working_capital, total_assets)  # Working Capital / Total Assets
                x2 = safe_divide(retained_earnings, total_assets)  # Retained Earnings / Total Assets
                x3 = safe_divide(ebit, total_assets)  # EBIT / Total Assets
                x4 = safe_divide(market_cap, total_liabilities)  # Market Value of Equity / Total Liabilities
                x5 = safe_divide(revenue, total_assets)  # Sales / Total Assets
                
                # Calculate Z-Score using Altman's formula
                z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
                
                result['score'] = round(z_score, 3)
                result['calculation_possible'] = True
                result['components'] = {
                    'Working_Capital_to_Total_Assets': round(x1, 3),
                    'Retained_Earnings_to_Total_Assets': round(x2, 3),
                    'EBIT_to_Total_Assets': round(x3, 3),
                    'Market_Value_to_Total_Liabilities': round(x4, 3),
                    'Sales_to_Total_Assets': round(x5, 3)
                }
                
                # Interpret the score
                if z_score > 2.99:
                    result['risk_level'] = 'LOW'
                    result['interpretation'] = 'Z-Score indicates Safe Zone. Low probability of bankruptcy.'
                elif z_score > 1.81:
                    result['risk_level'] = 'MEDIUM'
                    result['interpretation'] = 'Z-Score indicates Grey Zone. Moderate risk of financial distress.'
                else:
                    result['risk_level'] = 'HIGH'
                    result['interpretation'] = 'Z-Score indicates Distress Zone. High probability of bankruptcy within 2 years.'
                
            except Exception as e:
                result['interpretation'] = f'Error calculating Z-Score components: {str(e)}'
            
            return result
            
        except Exception as e:
            return {
                'score': None,
                'interpretation': f'Error calculating Z-Score: {str(e)}',
                'risk_level': 'UNKNOWN',
                'components': {},
                'calculation_possible': False
            }
    
    def analyze_promoter_pledge(self) -> Dict[str, Any]:
        """
        Analyze promoter pledge and insider ownership patterns
        
        Returns:
            Dictionary with pledge analysis
        """
        shareholding = self.financial_data.get('shareholding', {})
        
        insider_ownership = shareholding.get('insider_ownership', 0)
        institutional_ownership = shareholding.get('institutional_ownership', 0)
        
        result = {
            'insider_ownership_percent': round(insider_ownership, 2),
            'institutional_ownership_percent': round(institutional_ownership, 2),
            'risk_level': 'LOW',
            'red_flags': [],
            'interpretation': ''
        }
        
        # Analyze insider ownership
        if insider_ownership < 1:
            result['red_flags'].append('Very low insider ownership (< 1%) - management may lack confidence')
            result['risk_level'] = 'MEDIUM'
        elif insider_ownership > 75:
            result['red_flags'].append('Very high insider ownership (> 75%) - potential corporate governance concerns')
            result['risk_level'] = 'MEDIUM'
        
        # Analyze institutional ownership
        if institutional_ownership < 10:
            result['red_flags'].append('Low institutional ownership (< 10%) - may indicate lack of institutional confidence')
        
        # Check for high short interest
        short_ratio = shareholding.get('short_ratio', 0)
        if short_ratio > 10:
            result['red_flags'].append(f'High short interest ratio ({short_ratio:.1f}) - significant bearish sentiment')
            result['risk_level'] = 'HIGH'
        
        if not result['red_flags']:
            result['interpretation'] = 'Shareholding pattern appears normal with no significant red flags.'
        else:
            result['interpretation'] = f"Found {len(result['red_flags'])} potential concerns in shareholding pattern."
        
        return result
    
    def detect_financial_red_flags(self) -> Dict[str, Any]:
        """
        Detect various red flags in financial statements
        
        Returns:
            Dictionary with detected red flags
        """
        red_flags = []
        risk_score = 0.0
        
        # Check key ratios
        ratios = self.financial_data.get('key_ratios', {})
        
        # 1. Declining profit margins
        profit_margin = ratios.get('profit_margin', 0)
        if profit_margin < 0:
            red_flags.append({
                'category': 'Profitability',
                'flag': 'Negative profit margin',
                'severity': 'HIGH',
                'value': f'{profit_margin:.2f}%'
            })
            risk_score += 0.2
        elif profit_margin < 5:
            red_flags.append({
                'category': 'Profitability',
                'flag': 'Low profit margin',
                'severity': 'MEDIUM',
                'value': f'{profit_margin:.2f}%'
            })
            risk_score += 0.1
        
        # 2. High debt-to-equity ratio
        debt_to_equity = ratios.get('debt_to_equity', 0)
        if debt_to_equity > 2:
            red_flags.append({
                'category': 'Leverage',
                'flag': 'High debt-to-equity ratio',
                'severity': 'HIGH',
                'value': f'{debt_to_equity:.2f}'
            })
            risk_score += 0.2
        elif debt_to_equity > 1:
            red_flags.append({
                'category': 'Leverage',
                'flag': 'Elevated debt-to-equity ratio',
                'severity': 'MEDIUM',
                'value': f'{debt_to_equity:.2f}'
            })
            risk_score += 0.1
        
        # 3. Low current ratio (liquidity concern)
        current_ratio = ratios.get('current_ratio', 0)
        if current_ratio < 1:
            red_flags.append({
                'category': 'Liquidity',
                'flag': 'Current ratio below 1 - potential liquidity issues',
                'severity': 'HIGH',
                'value': f'{current_ratio:.2f}'
            })
            risk_score += 0.2
        elif current_ratio < 1.5:
            red_flags.append({
                'category': 'Liquidity',
                'flag': 'Low current ratio',
                'severity': 'MEDIUM',
                'value': f'{current_ratio:.2f}'
            })
            risk_score += 0.1
        
        # 4. Negative ROE
        roe = ratios.get('roe', 0)
        if roe < 0:
            red_flags.append({
                'category': 'Profitability',
                'flag': 'Negative Return on Equity',
                'severity': 'HIGH',
                'value': f'{roe:.2f}%'
            })
            risk_score += 0.15
        
        # 5. Check for revenue growth
        if not self.income_statement.empty and len(self.income_statement.columns) >= 2:
            revenue_current = self._get_value(self.income_statement, 'Total Revenue', 0)
            revenue_previous = self._get_value(self.income_statement, 'Total Revenue', 1)
            revenue_growth = calculate_percentage_change(revenue_current, revenue_previous)
            
            if revenue_growth < -10:
                red_flags.append({
                    'category': 'Growth',
                    'flag': 'Significant revenue decline',
                    'severity': 'HIGH',
                    'value': f'{revenue_growth:.2f}%'
                })
                risk_score += 0.15
        
        # Cap risk score at 1.0
        risk_score = min(risk_score, 1.0)
        
        return {
            'red_flags': red_flags,
            'total_flags': len(red_flags),
            'risk_score': round(risk_score, 2),
            'risk_level': 'HIGH' if risk_score > 0.6 else 'MEDIUM' if risk_score > 0.3 else 'LOW'
        }
    
    def _get_value(self, df: pd.DataFrame, row_name: str, col_index: int) -> float:
        """
        Safely extract value from financial dataframe
        
        Args:
            df: DataFrame to extract from
            row_name: Row name to look for
            col_index: Column index
            
        Returns:
            Extracted value or 0
        """
        try:
            if df.empty or col_index >= len(df.columns):
                return 0.0
            
            # Try exact match first
            if row_name in df.index:
                value = df.loc[row_name].iloc[col_index]
                return float(value) if not pd.isna(value) else 0.0
            
            # Try case-insensitive match
            for idx in df.index:
                if str(idx).lower() == row_name.lower():
                    value = df.loc[idx].iloc[col_index]
                    return float(value) if not pd.isna(value) else 0.0
            
            return 0.0
        except Exception:
            return 0.0
    
    def generate_forensic_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive forensic analysis report
        
        Returns:
            Dictionary with complete forensic analysis
        """
        print("Calculating Beneish M-Score...")
        m_score = self.calculate_beneish_m_score()
        
        print("Calculating Altman Z-Score...")
        z_score = self.calculate_altman_z_score()
        
        print("Analyzing promoter pledge...")
        pledge_analysis = self.analyze_promoter_pledge()
        
        print("Detecting financial red flags...")
        red_flags = self.detect_financial_red_flags()
        
        # Calculate overall risk score
        risk_scores = []
        if m_score['calculation_possible']:
            risk_scores.append(1.0 if m_score['risk_level'] == 'HIGH' else 0.3)
        if z_score['calculation_possible']:
            risk_scores.append(1.0 if z_score['risk_level'] == 'HIGH' else 0.5 if z_score['risk_level'] == 'MEDIUM' else 0.2)
        risk_scores.append(red_flags['risk_score'])
        
        overall_risk_score = np.mean(risk_scores) if risk_scores else 0.5
        
        return {
            'timestamp': datetime.now().isoformat(),
            'symbol': self.financial_data.get('symbol', 'N/A'),
            'beneish_m_score': m_score,
            'altman_z_score': z_score,
            'promoter_pledge_analysis': pledge_analysis,
            'financial_red_flags': red_flags,
            'overall_risk_score': round(overall_risk_score, 2),
            'overall_risk_level': 'HIGH' if overall_risk_score > 0.6 else 'MEDIUM' if overall_risk_score > 0.3 else 'LOW'
        }
