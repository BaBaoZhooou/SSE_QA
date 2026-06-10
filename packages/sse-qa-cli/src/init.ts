import { existsSync, mkdirSync, writeFileSync } from "node:fs";

import {
  configHome,
  configYamlPath,
  defaultConfigTemplate,
  defaultSecretsTemplate,
  secretsEnvPath,
} from "./config.js";

export interface InitOptions {
  force?: boolean;
}

export function runInit(options: InitOptions = {}): { created: string[]; skipped: string[] } {
  const home = configHome();
  mkdirSync(home, { recursive: true });
  const created: string[] = [];
  const skipped: string[] = [];

  const configPath = configYamlPath();
  if (existsSync(configPath) && !options.force) {
    skipped.push(configPath);
  } else {
    writeFileSync(configPath, defaultConfigTemplate(), "utf8");
    created.push(configPath);
  }

  const secretsPath = secretsEnvPath();
  if (existsSync(secretsPath) && !options.force) {
    skipped.push(secretsPath);
  } else {
    writeFileSync(secretsPath, defaultSecretsTemplate(), "utf8");
    created.push(secretsPath);
  }

  return { created, skipped };
}
