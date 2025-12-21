import { useState } from "react";

export function useForm<T>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    const keys = name.split(".");
    setValues(prev => {
      if (keys.length === 2) {
        const [parent, child] = keys;
        return {
          ...prev,
          [parent]: {
            ...((prev as any)[parent]),
            [child]:
              child === "base_price" || child === "stock" || child === "category_id"
                ? Number(value)
                : value,
          },
        };
      }
      return {
        ...prev,
        [name]:
          name === "base_price" || name === "stock" || name === "category_id"
            ? Number(value)
            : value,
      };
    });
  };

  const reset = () => setValues(initialValues);

  return {
    values,
    setValues,
    handleChange,
    reset,
  };
}
