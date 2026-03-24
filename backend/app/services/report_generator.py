"""PDF Report Generation Service"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
from typing import Dict
from ..config import settings

class ReportGenerator:
    """Generate PDF reports for SIMDCCO"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0A2463'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0A2463'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='Justified',
            parent=self.styles['BodyText'],
            alignment=TA_JUSTIFY,
            fontSize=11,
            leading=14
        ))
    
    def generate_organizational_report(
        self,
        organization_name: str,
        analytics_data: Dict,
        report_number: str,
        output_path: str = None
    ) -> str:
        """
        Generate organizational diagnostic report.
        
        Args:
            organization_name: Name of the organization
            analytics_data: Dictionary with analytics results
            report_number: Unique report number (e.g., SIMDCCO-2026-00001)
            output_path: Optional custom output path
        
        Returns:
            Path to generated PDF file
        """
        # Generate filename
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"relatorio_{organization_name}_{timestamp}.pdf"
            output_path = os.path.join(settings.REPORTS_DIR, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build content
        story = []
        
        # Header
        story.append(Paragraph("SIMDCCO", self.styles['CustomTitle']))
        story.append(Paragraph(
            "Sistema de Diagnóstico de Saúde Mental, Clima e Cultura Organizacional",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.5*cm))
        
        # Report info
        story.append(Paragraph(f"<b>Relatório:</b> {report_number}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Organização:</b> {organization_name}", self.styles['Normal']))
        story.append(Paragraph(
            f"<b>Data de Emissão:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 1*cm))
        
        # Executive Summary
        story.append(Paragraph("SUMÁRIO EXECUTIVO", self.styles['CustomSubtitle']))
        
        respondent_count = analytics_data.get('respondent_count', 0)
        imco_overall = analytics_data.get('imco_scores', {}).get('overall', 0)
        fdac_overall = analytics_data.get('fdac_scores', {}).get('overall', 0)
        risk_level = analytics_data.get('risk_level', 'low')
        
        risk_labels = {
            'low': 'Baixo Risco',
            'medium': 'Médio Risco',
            'high': 'Alto Risco',
            'critical': 'Risco Crítico'
        }
        
        summary_text = f"""
        Este relatório apresenta o diagnóstico organizacional realizado através do SIMDCCO,
        ferramenta desenvolvida com base em metodologias cientificamente validadas (IMCO e FDAC)
        para avaliação de clima e cultura organizacional, em conformidade com a NR-01
        (Gerenciamento de Riscos Ocupacionais).
        <br/><br/>
        <b>Total de Respondentes:</b> {respondent_count}<br/>
        <b>Score Geral IMCO (Clima):</b> {imco_overall:.2f}/5.0<br/>
        <b>Score Geral FDAC (Cultura):</b> {fdac_overall:.2f}/5.0<br/>
        <b>Classificação de Risco Psicossocial:</b> {risk_labels.get(risk_level, risk_level)}
        """
        story.append(Paragraph(summary_text, self.styles['Justified']))
        story.append(Spacer(1, 1*cm))
        
        # IMCO Results
        story.append(Paragraph("RESULTADOS IMCO - Clima Organizacional", self.styles['CustomSubtitle']))
        
        imco_vectors = analytics_data.get('imco_scores', {}).get('vectors', {})
        if imco_vectors:
            # Create table with vectors
            data = [['Vetor', 'Score']]
            for vector, score in sorted(imco_vectors.items()):
                data.append([vector, f"{score:.2f}"])
            
            table = Table(data, colWidths=[12*cm, 4*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A2463')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
            ]))
            story.append(table)
            story.append(Spacer(1, 1*cm))
        
        # FDAC Results
        story.append(Paragraph("RESULTADOS FDAC - Cultura Organizacional", self.styles['CustomSubtitle']))
        
        fdac_dimensions = analytics_data.get('fdac_scores', {}).get('dimensions', {})
        if fdac_dimensions:
            data = [['Dimensão', 'Score']]
            for dimension, score in sorted(fdac_dimensions.items()):
                data.append([dimension, f"{score:.2f}"])
            
            table = Table(data, colWidths=[12*cm, 4*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#15803D')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
            ]))
            story.append(table)
            story.append(Spacer(1, 1*cm))
        
        # Legal Framework
        story.append(PageBreak())
        story.append(Paragraph("BASE LEGAL - NR-01", self.styles['CustomSubtitle']))
        
        legal_text = """
        A Norma Regulamentadora NR-01 (Gerenciamento de Riscos Ocupacionais) estabelece
        a obrigatoriedade de identificar, avaliar e controlar riscos ocupacionais,
        incluindo os riscos psicossociais relacionados à saúde mental no trabalho.
        <br/><br/>
        Este relatório documenta formalmente a avaliação de riscos psicossociais realizada,
        servindo como evidência documental do cumprimento das obrigações legais estabelecidas
        pela NR-01. Os dados foram coletados de forma anônima, com consentimento LGPD registrado,
        e processados através de metodologias cientificamente validadas (IMCO e FDAC).
        """
        story.append(Paragraph(legal_text, self.styles['Justified']))
        story.append(Spacer(1, 1*cm))
        
        # Recommendations
        story.append(Paragraph("RECOMENDAÇÕES", self.styles['CustomSubtitle']))
        
        recommendations = self._generate_recommendations(analytics_data)
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['Normal']))
            story.append(Spacer(1, 0.3*cm))
        
        story.append(Spacer(1, 1*cm))
        
        # Footer
        story.append(Paragraph(
            "<i>Este relatório foi gerado automaticamente pelo Sistema SIMDCCO. "
            "Para mais informações, entre em contato com o administrador do sistema.</i>",
            self.styles['Normal']
        ))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _generate_recommendations(self, analytics_data: Dict) -> list:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        risk_level = analytics_data.get('risk_level', 'low')
        imco_overall = analytics_data.get('imco_scores', {}).get('overall', 0)
        
        if risk_level in ['high', 'critical']:
            recommendations.append(
                "Identificado risco psicossocial elevado. Recomenda-se intervenção imediata "
                "com apoio de profissionais de saúde ocupacional e RH."
            )
        
        if imco_overall < 3.0:
            recommendations.append(
                "Clima organizacional abaixo do ideal. Sugerimos implementar ações de "
                "melhoria focadas em comunicação, liderança e reconhecimento."
            )
        
        # Check low scoring vectors
        imco_vectors = analytics_data.get('imco_scores', {}).get('vectors', {})
        low_vectors = [v for v, s in imco_vectors.items() if s < 3.0]
        
        if low_vectors:
            recommendations.append(
                f"Vetores com scores críticos identificados: {', '.join(low_vectors)}. "
                "Ações direcionadas são necessárias nestas áreas."
            )
        
        if not recommendations:
            recommendations.append(
                "Organização apresenta indicadores positivos de clima e cultura. "
                "Manter monitoramento periódico para sustentação dos resultados."
            )
        
        return recommendations


# Singleton instance
report_generator = ReportGenerator()
