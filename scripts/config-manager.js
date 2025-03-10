const fs = require('fs');
const readline = require('readline');
const path = require('path');
const axios = require('axios');
const { spawn, execSync } = require('child_process');
const dotenv = require('dotenv');
const os = require('os');

const envDefaultFilePath = path.join(__dirname, '../.env.default');
const envFilePath = path.join(__dirname, '../.env');
const modelsLocalPath = path.join(__dirname, 'modelsLocalList.json');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const askQuestion = (query, defaultValue) => {
  return new Promise((resolve) => {
    rl.question(`${query} (default: ${defaultValue}): `, (answer) => {
      resolve(answer.trim() || defaultValue);
    });
  });
};

const displayDatabaseUrl = (user, password, db, port = '5432') => {
  console.log(`Database connection string: postgresql://${user}:${password}@localhost:${port}/${db}`);
};

const loadEnv = () => {
  const envData = fs.readFileSync(envDefaultFilePath, 'utf8');
  return envData.split('\n').reduce((acc, line) => {
    if (line && !line.startsWith('#')) {
      const [key, value] = line.split('=');
      acc[key.trim()] = value ? value.trim() : '';
    }
    return acc;
  }, {});
};

const loadJsonFile = (filePath) => {
  return fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath, 'utf8')) : {};
};

const startDocker = () => {
  return new Promise((resolve, reject) => {
    console.log('Starting Docker containers...');

    // Load environment variables from .env
    dotenv.config({ path: './.env' });

    const dockerProcess = spawn('docker', ['compose', 'up', '--build'], {
      stdio: 'inherit',
      env: process.env // Pass modified environment variables
    });

    dockerProcess.on('error', (error) => {
      reject(error);
    });
  });
};

// -------------------
// MACHINE CONFIGURATION
// -------------------

// Detect if the machine uses NUMA (Linux-specific)
function detectNUMA() {
  if (process.platform === 'linux') {
    try {
      const nodes = fs.readdirSync('/sys/devices/system/node/').filter(dir => /^node\d+$/.test(dir));
      return nodes.length > 1;
    } catch (err) {
      return false;
    }
  }
  return false;
}

// Detect the number of GPUs (using nvidia-smi)
function detectGPUs() {
  try {
    const output = execSync('nvidia-smi -L', { encoding: 'utf8' });
    const matches = output.match(/GPU \d+:/g);
    return matches ? matches.length : 0;
  } catch (err) {
    return 0;
  }
}

// Set machine-specific configuration values in the newConfig object
function setMachineConfig(newConfig) {
  const numCPUs = os.cpus().length;
  const totalMemory = os.totalmem();
  const numGPUs = detectGPUs();

  // Machine-specific settings
  newConfig['OLLAMA_LOCAL_MODEL_NUMA'] = detectNUMA().toString(); // true if multiple NUMA nodes detected
  newConfig['OLLAMA_LOCAL_MODEL_NUM_BATCH'] = Math.ceil(numCPUs / 2).toString(); // e.g., half the number of CPUs
  newConfig['OLLAMA_LOCAL_MODEL_NUM_GPU'] = numGPUs > 0 ? numGPUs.toString() : 'None'; // number of GPUs detected
  newConfig['OLLAMA_LOCAL_MODEL_MAIN_GPU'] = numGPUs > 0 ? '0' : 'None'; // use GPU 0 if available
  newConfig['OLLAMA_LOCAL_MODEL_LOW_VRAM'] = (totalMemory < 8 * 1024 * 1024 * 1024).toString(); // low VRAM mode if memory < 8GB
  newConfig['OLLAMA_LOCAL_MODEL_USE_MAP'] = process.platform === 'linux' ? 'true' : 'false'; // enable mmap on Linux
  newConfig['OLLAMA_LOCAL_MODEL_USE_LOCK'] = process.platform === 'linux' ? 'true' : 'false'; // enable mlock on Linux
  newConfig['OLLAMA_LOCAL_MODEL_NUM_THREAD'] = numCPUs.toString(); // number of CPU threads

  console.log('\nMachine-specific configuration:');
  console.log('NUMA:', newConfig['OLLAMA_LOCAL_MODEL_NUMA']);
  console.log('NUM_BATCH:', newConfig['OLLAMA_LOCAL_MODEL_NUM_BATCH']);
  console.log('NUM_GPU:', newConfig['OLLAMA_LOCAL_MODEL_NUM_GPU']);
  console.log('MAIN_GPU:', newConfig['OLLAMA_LOCAL_MODEL_MAIN_GPU']);
  console.log('LOW_VRAM:', newConfig['OLLAMA_LOCAL_MODEL_LOW_VRAM']);
  console.log('USE_MAP:', newConfig['OLLAMA_LOCAL_MODEL_USE_MAP']);
  console.log('USE_LOCK:', newConfig['OLLAMA_LOCAL_MODEL_USE_LOCK']);
  console.log('NUM_THREAD:', newConfig['OLLAMA_LOCAL_MODEL_NUM_THREAD']);
}

// -------------------
// CONFIGURE ENVIRONMENT
// -------------------

const configureEnvironment = async () => {
  // If .env already exists, skip setup
  if (fs.existsSync(envFilePath)) {
    console.log('🟢 Configuration found. Skipping setup...');
    await startDocker();
    process.exit(0); // Stop script execution
  }
  
  console.log('Configuring environment variables...');
  const envVariables = loadEnv();
  const modelsLocal = loadJsonFile(modelsLocalPath);
  const newConfig = { ...envVariables };

  // PostgreSQL Configuration
  console.log('\nConfiguring PostgreSQL:');
  newConfig['POSTGRES_USER'] = await askQuestion('Set POSTGRES_USER', envVariables['POSTGRES_USER']);
  newConfig['POSTGRES_PASSWORD'] = await askQuestion('Set POSTGRES_PASSWORD', envVariables['POSTGRES_PASSWORD']);
  newConfig['POSTGRES_DB'] = await askQuestion('Set POSTGRES_DB', envVariables['POSTGRES_DB']);
  displayDatabaseUrl(
    newConfig['POSTGRES_USER'],
    newConfig['POSTGRES_PASSWORD'],
    newConfig['POSTGRES_DB']
  );

  // AI Model Configuration
  console.log('\nAvailable local AI models:');
  const allModels = modelsLocal.developers.flatMap(dev => 
    dev.models.flatMap(m => m.versions.map(v => ({
      name: `${m.model_name}:${v.model_size}`,
      size: v.file_size
    })))
  );
  
  allModels.forEach((model, index) => 
    console.log(`${index + 1}. ${model.name} (${model.size})`)
  );
  
  const modelIndex = await askQuestion(`Select a local model (1-${allModels.length})`, envVariables['OLLAMA_LOCAL_MODEL_NAME']);
  newConfig['OLLAMA_LOCAL_MODEL_NAME'] = allModels[parseInt(modelIndex) - 1]?.name || envVariables['OLLAMA_LOCAL_MODEL_NAME'];
  console.log(`Selected local model: ${newConfig['OLLAMA_LOCAL_MODEL_NAME']}`);

  // --- Add machine-specific configuration ---
  setMachineConfig(newConfig);

  // Generate the .env file from newConfig
  const generateEnvOverride = (config) => {
    const envOverridePath = path.join(__dirname, '../.env');
  
    const envData = Object.entries(config)
      .map(([key, value]) => `${key}=${value}`)
      .join('\n');
  
    fs.writeFileSync(envOverridePath, envData);
    console.log(`✅ The .env file was generated successfully.`);
  };
  
  generateEnvOverride(newConfig);
  
  rl.close();
  
  // Start Docker
  try {
    await startDocker();
  } catch (error) {
    console.error('Failed to start Docker:', error);
    process.exit(1);
  }
};

configureEnvironment().catch(error => {
  console.error('Configuration failed:', error);
  process.exit(1);
});
