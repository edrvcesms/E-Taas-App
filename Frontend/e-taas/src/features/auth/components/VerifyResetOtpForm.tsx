import { verifyPasswordResetOtp } from '../../../services/auth/ResetPassword';
import { useForm } from '../../../hooks/general/useForm';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const VerifyResetOtpForm: React.FC = () => {

  const navigate = useNavigate();
  const { values, handleChange, reset } = useForm<{ otp: string }>({
    otp: '',
  });
  
  const stored_email = sessionStorage.getItem('resetEmail');
  useEffect(() => {
    if (!stored_email) {
      navigate('/forgot-password');
    }
  }, [navigate, stored_email]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (!stored_email) {
        return;
      }
      await verifyPasswordResetOtp(stored_email, values.otp);
      sessionStorage.setItem('verifiedResetEmail', stored_email);
      reset();
      navigate('/reset-password');
    } catch (error) {
      alert('OTP verification failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">OTP</label>
        <input
          type="text"
          name="otp"
          value={values.otp}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
          placeholder="Enter the OTP"
        />
      </div>
      <button
        type="submit"
        className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold"
      >
        Verify Otp
      </button>
    </form>
  );
};