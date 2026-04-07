/**
 * Validation schemas using Yup
 * Reusable validation rules for forms across the application.
 * Factory functions accept an i18n `t` function so that error messages
 * are rendered in the currently active locale.
 */

import * as yup from 'yup';

// ─────────────────────────────────────────────────────────────
// Static schemas (English only – used as a fallback when no i18n
// context is available, e.g. in unit tests that don't set up i18n).
// ─────────────────────────────────────────────────────────────

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

// ─────────────────────────────────────────────────────────────
// i18n-aware factory functions
// ─────────────────────────────────────────────────────────────

/**
 * Create an i18n-aware email schema.
 * @param t - The vue-i18n translation function
 */
export const createEmailSchema = (t: (key: string, values?: Record<string, unknown>) => string) =>
  yup
    .string()
    .required(t('validation.emailRequired'))
    .email(t('validation.emailInvalid'))
    .max(120, t('validation.emailMaxLength'))
    .trim();

/**
 * Create an i18n-aware password schema (strict – for registration).
 * @param t - The vue-i18n translation function
 */
export const createPasswordSchema = (t: (key: string, values?: Record<string, unknown>) => string) =>
  yup
    .string()
    .required(t('validation.passwordRequired'))
    .min(8, t('validation.passwordMin'))
    .matches(/[A-Z]/, t('validation.passwordUppercase'))
    .matches(/[a-z]/, t('validation.passwordLowercase'))
    .matches(/[0-9]/, t('validation.passwordDigit'))
    .matches(/[!@#$%^&*(),.?":{}|<>]/, t('validation.passwordSpecialChar'));

/**
 * Create an i18n-aware login form validation schema.
 * @param t - The vue-i18n translation function
 */
export const createLoginSchema = (t: (key: string, values?: Record<string, unknown>) => string) =>
  yup.object({
    email: createEmailSchema(t),
    password: yup.string().required(t('validation.loginPasswordRequired')),
  });

/**
 * Create an i18n-aware registration form validation schema.
 * @param t - The vue-i18n translation function
 */
export const createRegisterSchema = (t: (key: string, values?: Record<string, unknown>) => string) =>
  yup.object({
    email: createEmailSchema(t),
    password: createPasswordSchema(t),
  });

