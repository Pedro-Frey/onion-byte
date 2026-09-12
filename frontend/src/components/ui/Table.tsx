import React from 'react';

export function Table({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-full overflow-auto">
      <table className="w-full text-sm text-left text-gray-500">
        {children}
      </table>
    </div>
  );
}

export function TableHeader({ children }: { children: React.ReactNode }) {
  return (
    <thead className="text-xs text-gray-700 uppercase bg-gray-50 border-b border-gray-200">
      <tr>{children}</tr>
    </thead>
  );
}

export function TableHead({ children }: { children: React.ReactNode }) {
  return <th className="px-6 py-3 font-medium text-gray-900">{children}</th>;
}

export function TableBody({ children }: { children: React.ReactNode }) {
  return <tbody>{children}</tbody>;
}

export function TableRow({ children, onClick }: { children: React.ReactNode, onClick?: () => void }) {
  return (
    <tr 
      onClick={onClick}
      className={`bg-white border-b border-gray-200 hover:bg-gray-50 ${onClick ? 'cursor-pointer' : ''}`}
    >
      {children}
    </tr>
  );
}

export function TableCell({ children, className = "", ...props }: React.TdHTMLAttributes<HTMLTableCellElement>) {
  return <td className={`px-6 py-4 ${className}`} {...props}>{children}</td>;
}
