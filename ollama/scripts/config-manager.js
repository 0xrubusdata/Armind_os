const fs = require('fs');
const readline = require('readline');
const path = require('path');
const axios = require('axios');
const { spawn } = require('child_process');
const dotenv = require('dotenv');

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

const displayDatabaseUrl = (user, password, db, port) => {
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

    // Charger les variables d'environnement à partir de .env
    dotenv.config({ path: './.env' });

    const dockerProcess = spawn('docker', ['compose', 'up', '--build'], {
      stdio: 'inherit',
      env: process.env // Passer les variables d'environnement modifiées
    });

    dockerProcess.on('error', (error) => {
      reject(error);
    });
  });
};

const configureEnvironment = async () => {
  // Check if config override exists and bypass setup
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

  const generateEnvOverride = (config) => {
    const envOverridePath = path.join(__dirname, '../.env');
  
    const envData = Object.entries(config)
      .map(([key, value]) => `${key}=${value}`)
      .join('\n');
  
    fs.writeFileSync(envOverridePath, envData);
    console.log(`✅ The .env file was generated successfully.`);
  };
  
  // Générer le fichier .env
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