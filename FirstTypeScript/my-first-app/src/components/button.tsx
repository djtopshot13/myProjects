import React from "react";

type ButtonProps = {
  style: React.CSSProperties;
  borderRadius: Record<string, number>;
  children: string;
}

export default function Button({style, children}: ButtonProps) {
  return (
    <button style={style}>
      {children}
    </button>
  );
}