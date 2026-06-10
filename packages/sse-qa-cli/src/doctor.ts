import { runSetupCheck, type SetupReport } from "./setup-check.js";

export type DoctorCheck = SetupReport["checks"][number] & { name: string };

export interface DoctorReport extends SetupReport {}

export async function runDoctor(): Promise<DoctorReport> {
  return runSetupCheck();
}
