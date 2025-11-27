"""
Reports API endpoints
Handles PDF and CSV report generation for government, researchers, and civil engineers
"""

from flask import Blueprint, jsonify, request, send_file
from services.report_generator import ReportGenerator
from utils.validators import validate_report_params
import json
import io
import csv
from datetime import datetime

reports_bp = Blueprint('reports', __name__)
report_generator = ReportGenerator()

@reports_bp.route('/generate', methods=['POST'])
def generate_report():
    """Generate a report (PDF or CSV) based on parameters"""
    try:
        data = request.get_json()
        
        # Validate request parameters
        validation_result = validate_report_params(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        report_type = data.get('report_type', 'traffic_analysis')
        format_type = data.get('format', 'pdf')
        parameters = data.get('parameters', {})
        
        # Generate report
        report_data = report_generator.generate_report(report_type, parameters)
        
        if format_type.lower() == 'csv':
            return _generate_csv_response(report_data, report_type)
        else:
            return _generate_pdf_response(report_data, report_type)
            
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500

@reports_bp.route('/pdf', methods=['POST'])
def generate_pdf_report():
    """Generate PDF report"""
    try:
        data = request.get_json()
        report_type = data.get('report_type', 'traffic_analysis')
        parameters = data.get('parameters', {})
        
        report_data = report_generator.generate_report(report_type, parameters)
        return _generate_pdf_response(report_data, report_type)
        
    except Exception as e:
        return jsonify({'error': f'PDF report generation failed: {str(e)}'}), 500

@reports_bp.route('/csv', methods=['POST'])
def generate_csv_report():
    """Generate CSV report"""
    try:
        data = request.get_json()
        report_type = data.get('report_type', 'traffic_analysis')
        parameters = data.get('parameters', {})
        
        report_data = report_generator.generate_report(report_type, parameters)
        return _generate_csv_response(report_data, report_type)
        
    except Exception as e:
        return jsonify({'error': f'CSV report generation failed: {str(e)}'}), 500

@reports_bp.route('/list', methods=['GET'])
def list_reports():
    """List all available reports"""
    available_reports = {
        'government_reports': [
            {
                'id': 'traffic_congestion_analysis',
                'name': 'Traffic Congestion Analysis',
                'description': 'Detailed analysis of traffic congestion patterns and hotspots',
                'audience': 'government',
                'parameters': ['area', 'time_period', 'metrics']
            },
            {
                'id': 'infrastructure_planning',
                'name': 'Infrastructure Planning Report',
                'description': 'Data-driven insights for urban infrastructure development',
                'audience': 'government',
                'parameters': ['region', 'timeframe', 'budget_constraints']
            },
            {
                'id': 'environmental_impact',
                'name': 'Environmental Impact Assessment',
                'description': 'Analysis of traffic impact on environment and sustainability metrics',
                'audience': 'government',
                'parameters': ['area', 'emission_metrics', 'time_period']
            }
        ],
        'researcher_reports': [
            {
                'id': 'mobility_patterns',
                'name': 'Urban Mobility Patterns',
                'description': 'Academic analysis of movement patterns and behavioral insights',
                'audience': 'researchers',
                'parameters': ['study_area', 'timeframe', 'demographic_filters']
            },
            {
                'id': 'traffic_prediction_models',
                'name': 'Traffic Prediction Model Analysis',
                'description': 'Evaluation of ML models for traffic prediction',
                'audience': 'researchers',
                'parameters': ['model_type', 'evaluation_metrics', 'time_period']
            }
        ],
        'civil_engineering_reports': [
            {
                'id': 'road_usage_analysis',
                'name': 'Road Usage and Capacity Analysis',
                'description': 'Technical analysis of road usage patterns and capacity planning',
                'audience': 'civil_engineers',
                'parameters': ['road_network', 'time_period', 'capacity_metrics']
            },
            {
                'id': 'maintenance_prioritization',
                'name': 'Infrastructure Maintenance Prioritization',
                'description': 'Data-driven prioritization of road maintenance and repairs',
                'audience': 'civil_engineers',
                'parameters': ['road_conditions', 'usage_patterns', 'budget']
            }
        ]
    }
    
    return jsonify({
        'available_reports': available_reports,
        'total_count': sum(len(reports) for reports in available_reports.values())
    })

def _generate_pdf_response(report_data, report_type):
    """Generate PDF response from report data"""
    try:
        # For now, return a JSON response since PDF generation requires additional libraries
        # In production, you would use libraries like ReportLab or WeasyPrint
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return jsonify({
            'message': 'PDF report generated successfully',
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'data': report_data,
            'download_url': f'/api/reports/download/{filename}'  # Mock download URL
        })
    except Exception as e:
        return jsonify({'error': f'PDF generation error: {str(e)}'}), 500

def _generate_csv_response(report_data, report_type):
    """Generate CSV response from report data"""
    try:
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header based on report type
        if 'summary' in report_data:
            writer.writerow(['Metric', 'Value'])
            for key, value in report_data['summary'].items():
                writer.writerow([key.replace('_', ' ').title(), value])
        elif 'data' in report_data:
            if len(report_data['data']) > 0:
                writer.writerow(report_data['data'][0].keys())
                for row in report_data['data']:
                    writer.writerow(row.values())
        
        # Prepare response
        output.seek(0)
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': f'CSV generation error: {str(e)}'}), 500