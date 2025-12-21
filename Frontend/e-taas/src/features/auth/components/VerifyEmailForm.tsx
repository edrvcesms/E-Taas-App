import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { verifyEmail } from '../../../services/auth/EmailVerificationService';
import type { EmailVerificationData } from '../../../types/auth/EmailVerification';

export const VerifyEmailForm: React.FC = () => {
  const navigate = useNavigate();
  const [otpValues, setOtpValues] = useState<string[]>(['', '', '', '', '', '']);
  const [invalid, setInvalid] = useState<string>('');
  const [timer, setTimer] = useState<number>(120);
  const [isResendDisabled, setIsResendDisabled] = useState<boolean>(true);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  const storedData = sessionStorage.getItem('registerData');

  useEffect(() => {
    if (!storedData) {
      navigate('/register');
    }
  }, [navigate, storedData]);

  useEffect(() => {
    if (timer > 0) {
      const interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setIsResendDisabled(false);
    }
  }, [timer]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const value = e.target.value;

    if (!/^\d*$/.test(value)) return;

    const newOtpValues = [...otpValues];
    newOtpValues[index] = value;
    setOtpValues(newOtpValues);
    setInvalid('');

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number) => {
    if (e.key === 'Backspace' && !otpValues[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const otp = otpValues.join('');
    
    if (otp.length !== 6) {
      setInvalid('Please enter all 6 digits');
      return;
    }

    if (!storedData) return;

    try {
      const { username, email, password } = JSON.parse(storedData);
      const verificationData: EmailVerificationData = {
        username,
        email,
        password,
        otp,
      };

      await verifyEmail(verificationData);
      sessionStorage.removeItem('registerData');
      setOtpValues(['', '', '', '', '', '']);
      navigate('/login');
    } catch (error) {
      setInvalid('Invalid OTP. Please try again.');
      setOtpValues(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
    }
  };

  const handleResendOTP = async () => {
    if (isResendDisabled || !storedData) return;

    try {
      // Add your resend OTP service call here
      setTimer(120);
      setIsResendDisabled(true);
      setOtpValues(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
      setInvalid('');
    } catch (error) {
      setInvalid('Failed to resend OTP. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-5">
        <label className="block text-sm font-medium text-gray-700 text-center">Enter 6-Digit OTP</label>
        <div className="flex gap-3 justify-center">
          {[...Array(6)].map((_, index) => (
            <input
              key={index}
              ref={(el) => { inputRefs.current[index] = el; }}
              className="w-12 h-14 text-center text-xl font-semibold border-2 border-gray-300 rounded-lg bg-gray-50 focus:bg-white focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
              type="text"
              maxLength={1}
              value={otpValues[index]}
              onChange={(e) => handleChange(e, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
            />
          ))}
        </div>
        {invalid && (
          <p className="text-sm text-red-600 text-center">{invalid}</p>
        )}
      </div>

      {timer > 0 && (
        <p className="text-sm text-gray-600 text-center">
          OTP expires in: <span className="font-semibold text-pink-600">{timer}s</span>
        </p>
      )}

      <button
        onClick={handleSubmit}
        className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold"
      >
        Verify Email
      </button>

      <div className="text-center text-sm text-gray-600">
        Didn't receive the code?{' '}
        <button
          type="button"
          onClick={handleResendOTP}
          disabled={isResendDisabled}
          className={`font-medium ${
            isResendDisabled
              ? 'text-gray-400 cursor-not-allowed'
              : 'text-pink-500 hover:text-pink-600 cursor-pointer'
          }`}
        >
          Resend
        </button>
      </div>
    </div>
  );
};