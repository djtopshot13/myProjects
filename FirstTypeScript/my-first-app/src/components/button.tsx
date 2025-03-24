import React from "react";
import { type Color } from "@/../../lib/types";



export default function Button() {
  React.useEffect(() => {
    fetch('httpssfasfsjfdsaf').then
    ((response) => response.json())
    .then((data: unknown) => console.log(data))
  }, []);
  return (
    <button>Click Me!</button>
  );
}