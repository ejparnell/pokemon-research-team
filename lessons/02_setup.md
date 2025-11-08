# Lesson 2: Setting Up Your Multi-Agent Research Lab

Cool beans, time to roll up our sleeves and get our hands dirty, so to speak. Now that we have an understanding at a high level of what multi-agent systems are and why they're so cool, let's set up our own Pokémon research lab. Channel your inner Nurse Joy and let's get started with the set up.

## System Requirements

Before we dive in, let's talk about what you'll need to run this bad boy. Since we're dealing with Large Language Models (LLMs) and they can be pretty compute-hungry creatures, we need to make sure your setup can handle the workload.

This is the wicked sh*itty part about working with LLMs locally, they are resource intensive. If you have a gaming PC or a nice coding workstation, you are in luck. However if you are like me and own a MacMini you may need a virtual machine in the cloud to run this project smoothly.

### Minimum Local Setup

If you're running this on your local machine, here's what I recommend:

- **CPU**: Intel i5/AMD Ryzen 5 or better (4+ cores)
- **RAM**: 8GB minimum, 16GB preferred (trust me, those Python processes add up fast)
- **Storage**: At least 2GB free space (for dependencies and generated data)
- **Internet**: Stable connection for PokéAPI calls and LLM requests
- **Operating System**: Windows 10+, macOS 10.15+, or any modern Linux distribution

### Recommended Cloud Options

Now, if your local machine is feeling a bit wimpy or you want to scale things up, cloud is the way to go. Here are some solid AWS options that won't break the bank:

#### AWS EC2 Instance Recommendations

**Budget-Friendly Option**: `t3.medium`

- **vCPUs**: 2
- **RAM**: 4GB  
- **Cost**: ~$30-40/month
- **Best for**: Learning and small experiments

**Recommended Option**: `t3.large`

- **vCPUs**: 2
- **RAM**: 8GB
- **Cost**: ~$60-70/month  
- **Best for**: Full project development and testing

**Power User Option**: `c5.xlarge`

- **vCPUs**: 4
- **RAM**: 8GB
- **Cost**: ~$150-180/month
- **Best for**: Heavy development and multiple concurrent agents

**Beast Mode**: `c5.2xlarge`

- **vCPUs**: 8
- **RAM**: 16GB
- **Cost**: ~$300-350/month
- **Best for**: Production-level multi-agent systems

> Note: Prices are based on mid-2024 AWS pricing and may vary by region. If you go with a different cloud provider (like GCP or Azure), look for similar instance types with comparable CPU and RAM specs.

#### Setting Up Your AWS Instance

If you decide to go the AWS route (which I totally recommend for this project), here's a quick setup guide:

1. **Launch EC2 Instance**:

   - Choose Amazon Linux 2 or Ubuntu 20.04 LTS
   - Select your instance type from above
   - Configure security group to allow SSH (port 22)

2. **Connect to Your Instance**:

    ```bash
    ssh -i your-key.pem ec2-user@your-instance-ip
    ```

3. **Update System Packages**:

   ```bash
   sudo yum update -y  # Amazon Linux
   # OR
   sudo apt update && sudo apt upgrade -y  # Ubuntu
   ```

4. **Install Python 3.8+**:

   ```bash
   # Amazon Linux
   sudo yum install python3 python3-pip git -y
   
   # Ubuntu  
   sudo apt install python3 python3-pip python3-venv git -y
   ```

> Note: Depending on your instance type and OS choice, package installation commands may vary slightly. Please use those good ol' whitepages in Amazon or other related docs if you hit a snag.

## Python Environment Setup

Alright, let's get Python configured properly. I'll be showcasing a virtual environment setup using `venv`, which is included with Python 3. It's lightweight and perfect for our needs. You can also use `conda` or `virtualenv` if you prefer.

### Step 1: Make your Repository

Whatever way you want to make your repo is up to you. If you just want to `git init` on a new folder, go for it. If you want to push your code to GitHub or another git hosting service, that's cool too.

First things first, create your project repo:

```bash
# Create a local repo and init it
mkdir pokemon-research-team
cd pokemon-research-team
git init

# Use GitHub to create a repo then clone it down
git clone https://github.com/your-username/pokemon-research-team.git
cd pokemon-research-team
```

### Step 2: Create a Virtual Environment

Now let's create our isolated Python playground:

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (this is important!)
source venv/bin/activate

# On Windows, use this instead:
# venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt now. That's your sign that you're in the virtual environment - think of it as your "research lab mode" indicator.

### Step 3: Install Dependencies

Here comes the fun part! Let's install all the tools our agents will need. Since you're building this from scratch, we'll install each package individually so you understand what each one does:

```bash
# Upgrade pip first (always a good idea)
pip install --upgrade pip

# Install the core framework for multi-agent systems
pip install pyautogen

# Install API integration tools
pip install requests>=2.31.0

# Install data analysis and manipulation tools
pip install pandas>=2.0.0 numpy>=1.24.0

# Install visualization libraries
pip install matplotlib>=3.7.0 seaborn>=0.12.0
```

Now, let me break down what we just installed and why each piece matters:

#### Core Dependencies Breakdown

**AutoGen Framework** (`pyautogen`)

- This is the star of the show - the framework that makes our multi-agent conversations possible
- Handles all the agent coordination and dialogue management
- **Important**: AutoGen has been updated! We're using the new import structure from the stable docs
- See [Microsoft AutoGen Stable Docs](https://microsoft.github.io/autogen/stable/) for reference

**API Integration** (`requests>=2.31.0`)

- Our gateway to the PokéAPI
- Handles all HTTP requests to fetch real-time Pokémon data

**Data Analysis Stack**:

- **Pandas** (`pandas>=2.0.0`): Data manipulation and analysis (think Excel but way more powerful)
- **NumPy** (`numpy>=1.24.0`): Numerical computing foundation
- **SciPy** (optional): Advanced statistical functions

**Visualization Tools**:

- **Matplotlib** (`matplotlib>=3.7.0`): Core plotting library
- **Seaborn** (`seaborn>=0.12.0`): Makes beautiful statistical visualizations

If everything installed correctly, you should see something like "Successfully installed..." with a bunch of package names.

**Pro Tip**: Now that you've installed everything, let's create a `requirements.txt` file so you (and others) can easily recreate this environment later:

```bash
# Create a requirements.txt file with all installed packages
pip freeze > requirements.txt
```

This creates a file listing all your installed packages and their exact versions. Super handy for sharing your project or setting it up on another machine!

If you run into any issues during installation, don't panic! Here are some common fixes:

#### Troubleshooting Installation Issues

**Problem**: Permission errors on macOS/Linux

```bash
# Solution: Use --user flag
pip install --user pyautogen requests>=2.31.0 pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.7.0 seaborn>=0.12.0
```

**Problem**: Slow downloads

```bash
# Solution: Use a different index
pip install -i https://pypi.org/simple/ pyautogen requests>=2.31.0 pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.7.0 seaborn>=0.12.0
```

**Problem**: Package conflicts

```bash
# Solution: Create a fresh environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install pyautogen requests>=2.31.0 pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.7.0 seaborn>=0.12.0
```

## Project Structure Setup

Now that we have our dependencies sorted, let's make sure our project structure is set up correctly. Think of this as organizing our research lab so everything has its proper place.

### Understanding the File Structure

Let's take a tour of what we've got:

```
pokemon-research-team/
├── README.md                   # Your project documentation
├── requirements.txt            # All those packages we just installed
├── setup.sh                    # Automated setup script
├── main.py                     # The main entry point here
├── src/                        # The heart of our system
│   ├── __init__.py             # Makes this a Python package
│   │
│   ├── agents/                 # Our AI agents live here
│   │   ├── __init__.py
│   │   ├── research_agents.py  # Professor Oak, Researcher, Reporter
│   │   └── coordinator.py      # Agent communication hub
│   │
│   ├── tools/                  # Utility tools and integrations
│   │   ├── __init__.py
│   │   ├── pokemon_api.py      # PokéAPI integration magic
│   │   └── visualizer.py       # Chart and graph generation
│   │
│   └── utils/                  # Shared utilities and helpers
│       └── __init__.py
│
├── examples/                   # Working examples and demos
│   └── fire_type_analysis.py   # Complete Fire-type research demo
│
└── data/                       # Generated outputs and cache
    └── visualizations/         # Charts, graphs, and reports go here
```

### Verifying Your Setup

Let's make sure everything is in the right place and working correctly:

```bash
# Check if Python can import our modules
python -c "import src.agents.research_agents; print('Agents module: OK')"
python -c "import src.tools.pokemon_api; print('API tools: OK')"
python -c "from examples.fire_type_analysis import simple_pokemon_lookup; print('Examples: OK')"

# Verify external dependencies
python -c "from autogen import AssistantAgent; print('AutoGen: OK')"
python -c "import requests; print('Requests: OK')"
python -c "import matplotlib; print('Matplotlib: OK')"
python -c "import pandas; print('Pandas: OK')"
```

If all those print "OK", you're golden! If not, double-check your virtual environment is activated and try reinstalling the problematic package.

### Creating Missing Directories

Sometimes directories don't get created automatically, so let's make sure they exist:

```bash
# Create data directories if they don't exist
mkdir -p data/visualizations
mkdir -p data/cache

# Make sure we can write to them
touch data/visualizations/test.txt
rm data/visualizations/test.txt
echo "Directory permissions: OK"
```

## API Keys and Configuration

Here's where things get a bit more serious. Our agents need to talk to external services, and that means we need some API keys.

### OpenAI API Key (Required for Full Functionality)

The AutoGen framework can use various LLM providers, but OpenAI is the most straightforward option:

1. **Get Your API Key**:
   - Head over to [OpenAI's website](https://openai.com/api/)
   - Sign up or log in
   - Navigate to API Keys section
   - Create a new API key

2. **Set Up Environment Variables**:

   ```bash
   # On macOS/Linux - add to your ~/.bashrc or ~/.zshrc
   export OPENAI_API_KEY="your-actual-api-key-here"
   
   # On Windows - use Command Prompt
   setx OPENAI_API_KEY "your-actual-api-key-here"
   ```

3. **Verify It's Working**:

   ```bash
   echo $OPENAI_API_KEY  # Should show your key (first few chars)
   ```

### Alternative: Local LLM Setup (Advanced)

If you don't want to use OpenAI or want to keep everything local, you can configure AutoGen to use local models like Ollama. This is more complex but totally doable:

```bash
# Install Ollama (macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (this will take a while)
ollama pull llama2

# Configure AutoGen to use local model (we'll cover this in the next lesson)
```

### PokéAPI (Free - No Key Required!)

Good news! The PokéAPI is completely free and doesn't require any API keys. It's one of the most developer-friendly APIs out there. Our system will automatically handle rate limiting and caching to be respectful of their servers.

## Setup Verification Checklist

Before moving on to the next lesson, let's make sure you've got everything sorted:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed from requirements.txt
- [ ] Project structure verified and directories created
- [ ] API keys configured (at least attempt OpenAI setup)

If you can check all those boxes, you're absolutely ready to start building your multi-agent system!

## 🎯 Performance Optimization Tips

Since we're dealing with LLMs and potentially multiple agents running simultaneously, here are some tips to keep things running smoothly:

### Memory Management

- **Monitor your RAM usage** - Multiple agents can be memory hungry
- **Use smaller models** for development (GPT-3.5 instead of GPT-4)
- **Implement caching** for API responses to avoid repeated requests

### API Rate Limiting

- **Respect API limits** - Both OpenAI and PokéAPI have rate limits
- **Implement exponential backoff** for failed requests
- **Use async programming** for concurrent API calls (advanced topic)

### Cost Management (If using OpenAI)

- **Set usage alerts** in your OpenAI dashboard
- **Use cheaper models for development** (GPT-3.5-turbo vs GPT-4)
- **Implement token counting** to track usage
- **Consider local models for heavy development**

## Next Steps: Time to Code

Ready to bring your agents to life? Let's dive into [Lesson 3: Building Your First Agent](lessons/03_building_agents.md) and start creating some AI magic.
