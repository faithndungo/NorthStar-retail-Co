import { ORDER_STEPS } from '../../utils/constants.js';

export default function ProgressSteps({ currentStep }) {
  return (
    <ol className="progress" aria-label="Order progress">
      {ORDER_STEPS.map((step, index) => {
        const state =
          index < currentStep ? 'complete' : index === currentStep ? 'active' : 'todo';
        return (
          <li key={step} className={`progress-step ${state}`}>
            {step}
          </li>
        );
      })}
    </ol>
  );
}