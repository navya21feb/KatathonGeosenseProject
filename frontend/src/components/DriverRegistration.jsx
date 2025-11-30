import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Camera, User, Car, FileText, Shield, CheckCircle, Sparkles } from 'lucide-react';
import './DriverRegistration.css';

const DriverRegistration = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    full_name: '',
    dob: '',
    phone: '',
    aadhaar: '',
    pan: '',
    dl_number: '',
    dl_validity: '',
    rc_number: '',
    vehicle_type: '',
    vehicle_make: '',
    vehicle_model: '',
    vehicle_year: ''
  });

  const [files, setFiles] = useState({
    selfie: null,
    dl_front: null,
    dl_back: null,
    rc_scan: null,
    insurance_scan: null,
    pollution_certificate: null
  });

  const [showCamera, setShowCamera] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const { name, files: fileList } = e.target;
    if (fileList && fileList[0]) {
      setFiles(prev => ({
        ...prev,
        [name]: fileList[0]
      }));
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'user',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        } 
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setShowCamera(true);
    } catch (err) {
      alert('Unable to access camera. Please check permissions.');
      console.error('Camera error:', err);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setShowCamera(false);
  };

  const captureSelfie = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(videoRef.current, 0, 0);
      
      canvas.toBlob((blob) => {
        const file = new File([blob], 'selfie.jpg', { type: 'image/jpeg' });
        setFiles(prev => ({
          ...prev,
          selfie: file
        }));
        stopCamera();
      }, 'image/jpeg', 0.9);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Show success modal instead of alert
      setShowSuccess(true);
      
    } catch (error) {
      alert('Registration failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSuccessClose = () => {
    setShowSuccess(false);
    onSuccess();
    
    // Reset form
    setFormData({
      full_name: '',
      dob: '',
      phone: '',
      aadhaar: '',
      pan: '',
      dl_number: '',
      dl_validity: '',
      rc_number: '',
      vehicle_type: '',
      vehicle_make: '',
      vehicle_model: '',
      vehicle_year: ''
    });
    setFiles({
      selfie: null,
      dl_front: null,
      dl_back: null,
      rc_scan: null,
      insurance_scan: null,
      pollution_certificate: null
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <motion.div 
        className="modal-content"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
      >
        <div className="modal-header">
          <div className="modal-title">
            <Shield size={24} className="modal-icon" />
            <h2>Driver Registration</h2>
          </div>
          <button className="close-button" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="driver-form">
          {/* Personal Information */}
          <div className="form-section">
            <div className="section-header">
              <User size={20} />
              <h3>Personal Information</h3>
            </div>
            <div className="form-grid">
              <div className="form-group">
                <label>Full Name *</label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Date of Birth *</label>
                <input
                  type="date"
                  name="dob"
                  value={formData.dob}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Phone Number *</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Aadhaar Number *</label>
                <input
                  type="text"
                  name="aadhaar"
                  value={formData.aadhaar}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>PAN Number *</label>
                <input
                  type="text"
                  name="pan"
                  value={formData.pan}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
          </div>

          {/* Selfie Verification */}
          <div className="form-section">
            <div className="section-header">
              <Camera size={20} />
              <h3>Selfie Verification</h3>
            </div>
            <div className="selfie-verification">
              {!files.selfie ? (
                <div className="selfie-upload-area">
                  <div className="selfie-instructions">
                    <Camera size={48} className="camera-icon" />
                    <h4>Take Selfie for Verification</h4>
                    <p>Please take a clear selfie for identity verification</p>
                  </div>
                  <button 
                    type="button" 
                    className="take-selfie-button"
                    onClick={startCamera}
                  >
                    <Camera size={20} />
                    Take Selfie
                  </button>
                </div>
              ) : (
                <div className="selfie-preview-container">
                  <h4>Selfie Preview</h4>
                  <div className="selfie-preview">
                    <h5>Selfie Captured 😊</h5>
                    <div className="selfie-actions">
                      <button 
                        type="button" 
                        className="retake-selfie-button"
                        onClick={() => {
                          setFiles(prev => ({ ...prev, selfie: null }));
                          startCamera();
                        }}
                      >
                        Retake
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Driving License Information */}
          <div className="form-section">
            <div className="section-header">
              <FileText size={20} />
              <h3>Driving License Information</h3>
            </div>
            <div className="form-grid">
              <div className="form-group">
                <label>DL Number *</label>
                <input
                  type="text"
                  name="dl_number"
                  value={formData.dl_number}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Validity Date *</label>
                <input
                  type="date"
                  name="dl_validity"
                  value={formData.dl_validity}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            <div className="file-upload-grid">
              <div className="file-upload-group">
                <label>DL Front Photo *</label>
                <label className="file-upload-label full-width">
                  {files.dl_front ? 'Change DL Front' : 'Upload DL Front'}
                  <input
                    type="file"
                    name="dl_front"
                    accept="image/*"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                </label>
                {files.dl_front && (
                  <span className="file-name">{files.dl_front.name}</span>
                )}
              </div>
              <div className="file-upload-group">
                <label>DL Back Photo *</label>
                <label className="file-upload-label full-width">
                  {files.dl_back ? 'Change DL Back' : 'Upload DL Back'}
                  <input
                    type="file"
                    name="dl_back"
                    accept="image/*"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                </label>
                {files.dl_back && (
                  <span className="file-name">{files.dl_back.name}</span>
                )}
              </div>
            </div>
          </div>

          {/* Vehicle Information */}
          <div className="form-section">
            <div className="section-header">
              <Car size={20} />
              <h3>Vehicle Information</h3>
            </div>
            <div className="form-grid">
              <div className="form-group">
                <label>RC Number *</label>
                <input
                  type="text"
                  name="rc_number"
                  value={formData.rc_number}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Vehicle Type *</label>
                <select
                  name="vehicle_type"
                  value={formData.vehicle_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Vehicle Type</option>
                  <option value="hatchback">Hatchback</option>
                  <option value="sedan">Sedan</option>
                  <option value="suv">SUV</option>
                  <option value="compact_suv">Compact SUV</option>
                  <option value="luxury">Luxury</option>
                  <option value="electric">Electric</option>
                </select>
              </div>
              <div className="form-group">
                <label>Vehicle Make *</label>
                <input
                  type="text"
                  name="vehicle_make"
                  value={formData.vehicle_make}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Vehicle Model *</label>
                <input
                  type="text"
                  name="vehicle_model"
                  value={formData.vehicle_model}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Vehicle Year *</label>
                <input
                  type="number"
                  name="vehicle_year"
                  value={formData.vehicle_year}
                  onChange={handleInputChange}
                  min="2000"
                  max="2024"
                  required
                />
              </div>
            </div>

            <div className="file-upload-grid">
              <div className="file-upload-group">
                <label>RC Scan *</label>
                <label className="file-upload-label full-width">
                  {files.rc_scan ? 'Change RC' : 'Upload RC'}
                  <input
                    type="file"
                    name="rc_scan"
                    accept="image/*,.pdf"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                </label>
                {files.rc_scan && (
                  <span className="file-name">{files.rc_scan.name}</span>
                )}
              </div>
              <div className="file-upload-group">
                <label>Insurance Scan *</label>
                <label className="file-upload-label full-width">
                  {files.insurance_scan ? 'Change Insurance' : 'Upload Insurance'}
                  <input
                    type="file"
                    name="insurance_scan"
                    accept="image/*,.pdf"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                </label>
                {files.insurance_scan && (
                  <span className="file-name">{files.insurance_scan.name}</span>
                )}
              </div>
              <div className="file-upload-group">
                <label>Pollution Certificate *</label>
                <label className="file-upload-label full-width">
                  {files.pollution_certificate ? 'Change PUC' : 'Upload PUC'}
                  <input
                    type="file"
                    name="pollution_certificate"
                    accept="image/*,.pdf"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                </label>
                {files.pollution_certificate && (
                  <span className="file-name">{files.pollution_certificate.name}</span>
                )}
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              className="cancel-button"
              onClick={onClose}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="submit-button"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Registering...' : 'Register and Verify as Driver'}
            </button>
          </div>
        </form>
      </motion.div>

      {/* Camera Modal */}
      {showCamera && (
        <div className="camera-modal">
          <div className="camera-content">
            <div className="camera-header">
              <h3>Take Selfie</h3>
              <button onClick={stopCamera}>×</button>
            </div>
            <div className="camera-preview">
              <video ref={videoRef} autoPlay playsInline className="camera-video" />
              <div className="camera-overlay">
                <div className="face-guide"></div>
              </div>
            </div>
            <div className="camera-controls">
              <button onClick={stopCamera} className="camera-cancel-button">
                Cancel
              </button>
              <button onClick={captureSelfie} className="capture-button">
                <Camera size={24} />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Success Modal */}
      <AnimatePresence>
        {showSuccess && (
          <div className="success-modal-overlay">
            <motion.div 
              className="success-modal-content"
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: -20 }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
            >
              <div className="success-animation">
                <div className="success-icon-container">
                  <CheckCircle className="success-icon" />
                  <div className="sparkle-effect">
                    <Sparkles className="sparkle" />
                  </div>
                </div>
              </div>
              
              <div className="success-content">
                <h2 className="success-title">Congratulations! 🎉</h2>
                <p className="success-message">
                  You have been successfully <strong>registered and verified as a driver</strong>!
                </p>
                <p className="success-submessage">
                  You can now start accepting ride requests and earn money with your vehicle.
                </p>
              </div>

              <div className="success-features">
                <div className="feature-item">
                  <CheckCircle size={16} className="feature-icon" />
                  <span>Profile Verified</span>
                </div>
                <div className="feature-item">
                  <CheckCircle size={16} className="feature-icon" />
                  <span>Documents Approved</span>
                </div>
                <div className="feature-item">
                  <CheckCircle size={16} className="feature-icon" />
                  <span>Ready to Drive</span>
                </div>
              </div>

              <button 
                className="success-button"
                onClick={handleSuccessClose}
              >
                Start Your Journey
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default DriverRegistration;