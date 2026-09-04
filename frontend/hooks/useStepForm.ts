import { useEffect, useState } from "react";
import type { FieldPath, UseFormSetFocus, UseFormTrigger } from "react-hook-form";
import z from "zod";

export default function useStepForm<T extends z.ZodObject<z.ZodRawShape>>(
  schema: T,
  trigger: UseFormTrigger<z.infer<T>>,
  setFocus: UseFormSetFocus<z.infer<T>>,
): {
  fields: readonly FieldPath<z.infer<T>>[];
  step: number;
  handleNextStep: () => Promise<void>;
  handleStepKeyDown: (event: React.KeyboardEvent) => void;
} {
  const fields = schema.keyof().options as unknown as readonly FieldPath<z.infer<T>>[];
  const [step, setStep] = useState(0);

  useEffect(() => {
    const currentField = fields[step];

    if (currentField) {
      setFocus(currentField);
    }
  }, [schema, step, setFocus]);

  async function handleNextStep() {
    const currentField = fields[step];
    if (!currentField) return;

    const valid = await trigger(currentField);
    if (!valid) return;

    if (step < fields.length - 1) {
      setStep((currentStep) => currentStep + 1);
    }
  }

  function handleStepKeyDown(event: React.KeyboardEvent) {
    if (event.key === "Enter") {
      event.preventDefault();
      void handleNextStep();
    }
  }

  return {
    fields,
    step,
    handleNextStep,
    handleStepKeyDown,
  };
}