/**
 * Sanitiza uma string removendo tags HTML perigosas para prevenir XSS
 * @param input String para sanitizar
 */
export function sanitizeInput(input: string): string {
  if (!input) return input;
  // Simples sanitização baseada em regex para remover tags script e html
  return input
    .replace(/<script[^>]*?>.*?<\/script>/gi, '')
    .replace(/<[\/\!]*?[^<>]*?>/gi, '')
    .replace(/javascript:/gi, '');
}

/**
 * Sanitiza recursivamente todos os valores string de um objeto
 * @param obj Objeto para sanitizar
 */
export function sanitizeObject<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return (typeof obj === 'string' ? sanitizeInput(obj) : obj) as T;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => sanitizeObject(item)) as unknown as T;
  }

  const sanitized = {} as Record<string, any>;
  for (const [key, value] of Object.entries(obj)) {
    sanitized[key] = sanitizeObject(value);
  }

  return sanitized as T;
}

/**
 * Simples ofuscação (Nota: num ambiente de produção real usaríamos HttpOnly Cookies)
 */
export function encryptToken(token: string): string {
  try {
    return btoa(token).split('').reverse().join('');
  } catch (e) {
    return token;
  }
}

/**
 * Desfaz a ofuscação
 */
export function decryptToken(encrypted: string): string {
  try {
    return atob(encrypted.split('').reverse().join(''));
  } catch (e) {
    return encrypted;
  }
}

export function validateEmail(email: string): boolean {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

/**
 * Validação básica de CPF brasileiro
 */
export function validateCPF(cpf: string): boolean {
  const cleanCPF = cpf.replace(/[^\d]+/g, '');
  if (cleanCPF.length !== 11 || /^(\d)\1{10}$/.test(cleanCPF)) return false;
  
  let sum = 0;
  for (let i = 1; i <= 9; i++) sum = sum + parseInt(cleanCPF.substring(i - 1, i)) * (11 - i);
  let rest = (sum * 10) % 11;
  if ((rest === 10) || (rest === 11)) rest = 0;
  if (rest !== parseInt(cleanCPF.substring(9, 10))) return false;

  sum = 0;
  for (let i = 1; i <= 10; i++) sum = sum + parseInt(cleanCPF.substring(i - 1, i)) * (12 - i);
  rest = (sum * 10) % 11;
  if ((rest === 10) || (rest === 11)) rest = 0;
  if (rest !== parseInt(cleanCPF.substring(10, 11))) return false;

  return true;
}

export function maskCPF(cpf: string): string {
  const v = cpf.replace(/\D/g, '');
  return v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
}

export function maskPhone(phone: string): string {
  const v = phone.replace(/\D/g, '');
  return v.replace(/^(\d{2})(\d{2})(\d{4,5})(\d{4}).*/, "+$1 ($2) $3-$4");
}
