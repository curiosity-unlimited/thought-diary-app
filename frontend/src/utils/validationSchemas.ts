/**
 * Validation schemas using Yup
 * Reusable validation rules for forms across the application
 */

import * as yup from 'yup';

/**
 * Email validation schema
 * - Required field
 * - Must be valid email format (RFC 5322)
 * - Maximum 120 characters
 */
export const emailSchema = yup
  .string()
  .required('Email is required')
  .email('Please enter a valid email address')
  .max(120, 'Email must not exceed 120 characters')
  .trim();

/**
 * Password validation schema
 * - Required field
 * - Minimum 8 characters
 * - Must contain at least one uppercase letter
 * - Must contain at least one lowercase letter
 * - Must contain at least one digit
 * - Must contain at least one special character
 */
export const passwordSchema = yup
  .string()
  .required('Password is required')
  .min(8, 'Password must be at least 8 characters')
  .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .matches(/[a-z]/, 'Password must contain at least one lowercase letter')
  .matches(/[0-9]/, 'Password must contain at least one digit')
  .matches(
    /[!@#$%^&*(),.?":{}|<>]/,
    'Password must contain at least one special character'
  );

/**
 * Login form validation schema
 */
export const loginSchema = yup.object({
  email: emailSchema,
  password: yup.string().required('Password is required'), // Less strict for login
});

/**
 * Registration form validation schema
 */
export const registerSchema = yup.object({
  email: emailSchema,
  password: passwordSchema, // Strict validation for registration
});
