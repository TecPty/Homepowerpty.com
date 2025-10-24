// Al final de appointment-system.tsx
export { default as AppointmentSystem } from './appointment-system';

import { WorkSessionTracker } from '@/components/employee/WorkSessionTracker';

export default function EmployeePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Bienvenido</h1>
      <p className="text-gray-600">Gestiona tu agenda y horarios de trabajo</p>

      <AppointmentSystem />
      <WorkSessionTracker />
    </div>
  );
}