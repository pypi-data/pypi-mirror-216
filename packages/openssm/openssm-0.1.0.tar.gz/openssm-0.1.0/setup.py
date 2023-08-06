# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openssm',
 'openssm.archive.models',
 'openssm.core',
 'openssm.core.adapter',
 'openssm.core.backend',
 'openssm.core.old_abstract',
 'openssm.core.slm',
 'openssm.core.slm.memory',
 'openssm.core.ssm',
 'openssm.old_ssm',
 'openssm.old_ssm.abstract']

package_data = \
{'': ['*'],
 'openssm': ['archive/training/*',
             'archive/training/fine_tuning/*',
             'archive/training/validation/*',
             'industrial/interpretability/*',
             'industrial/monitoring/*',
             'industrial/security/*',
             'industrial/security/audit/*',
             'industrial/security/best_practices/*',
             'integration/*',
             'integration/llamaindex/*',
             'integration/testing_tools/*'],
 'openssm.archive.models': ['pre_trained/*',
                            'user_trained/*',
                            'validation/*',
                            'version_control/*']}

setup_kwargs = {
    'name': 'openssm',
    'version': '0.1.0',
    'description': "OpenSSM – 'Small Specialist Models' for Industrial AI",
    'long_description': '## OpenSSM – “Small Specialist Models” for Industrial AI\nOpenSSM (pronounced `open-ess-ess-em`) is an open-source framework for Small Specialist Models (SSMs), which are key to enhancing\ntrust, reliability, and safety in Industrial-AI applications. Harnessing the power of domain expertise, SSMs operate either\nalone or in "teams". They collaborate with other SSMs, planners, and sensors/actuators to deliver real-world problem-solving\ncapabilities.\n\nUnlike Large Language Models (LLMs), which are computationally intensive and generalized, SSMs are lean, efficient, and\ndesigned specifically for individual domains. This focus makes them an optimal choice for businesses, SMEs, researchers,\nand developers seeking specialized and robust AI solutions for industrial applications.\n\n![SSM in Industrial AI](./diagrams/ssm-industrial-use-case.drawio.png)\n\nA prime deployment scenario for SSMs is within the aiCALM (Collaborative Augmented Large Models) architecture. aiCALM\nrepresents a cohesive assembly of AI components tailored for sophisticated problem-solving capabilities. Within this\nframework, SSMs work with General Management Models (GMMs) and other components to solve complex, domain-specific, and\nindustrial problems.\n\n## Why SSM?\nThe trend towards specialization in AI models is a clear trajectory seen by many in the field.\n\n> Specialization is crucial for quality .. not general purpose Al models – Eric Schmidt, Schmidt Foundation\n\n> .. small models .. for a specific task that are good –  Matei Zaharia, Databricks\n\n> .. small agents working together .. specific and best in their tasks – Harrison Chase, Langchain\n\n> .. small but highly capable expert models – Andrej Karpathy, OpenAI\n\n> .. small models are .. a massive paradigm shift .. about deploying AI models at scale – Rob Toews, Radical Ventures\n\nAs predicted by Eric Schmidt and others, we will see “a rich ecosystem to emerge [of] high-value, specialized AI systems.”\nSSMs are the central part in the architecture of these systems.\n\n## What OpenSSM Offers\nOpenSSM fills this gap directly, with the following benefits to the community, developers, and businesses:\n\n- **Industrial Focus:** SSMs are developed with a specific emphasis on industrial applications, addressing the unique\nrequirements of trustworthiness, safety, reliability, and scalability inherent to this sector.\n\n- **Fast, Cost-Effective & Easy to Use:** SSMs are 100-1000x faster and more efficient than LLMs, making them accessible\nand cost-effective particularly for industrial usage where time and resources are critical factors.\n\n- **Easy Knowledge Capture:** OpenSSM has easy-to-use tools for capturing domain knowledge in diverse forms: books, operaring manuals, databases, knowledge graphs, text files, and code.\n\n- **Powerful Operations on Captured Knowledge:** OpenSSM enables both knowledge query and inferencing/predictive capabilities based on the domain-specific knowledge.\n\n- **Collaborative Problem-Solving**: SSMs are designed to work in problem-solving "teams". Multi-SSM collaboration is a first-class design feature, not an afterthought.\n\n- **Reliable Domain Expertise:** Each SSM has expertise in a particular field or equipment, offering precise and specialized\nknowledge, thereby enhancing trustworthiness, reliability, and safety for Industrial-AI applications. With self-reasoning,\ncausal reasoning, and retrieval-based knowledge, SSMs provide a trustable source of domain expertise.\n\n- **Vendor Independence:** OpenSSM allows everyone to build, train, and deploy their own domain-expert AI models, offering\nfreedom from vendor lock-in and security concerns.\n\n- **Composable Expertise**: SSMs are fully composable, making it easy to combine domain expertise.\n\n## Target Audience\nOur primary audience includes:\n\n- **Businesses and SMEs** wishing to leverage AI in their specific industrial context without relying on extensive\ncomputational resources or large vendor solutions.\n\n- **AI researchers and developers** keen on creating more efficient, robust, and domain-specific AI models for industrial applications.\n\n- **Open-source contributors** believing in democratizing industrial AI and eager to contribute to a community-driven\nproject focused on building and sharing specialized AI models.\n\n- **Industries** with specific domain problems that can be tackled more effectively by a specialist AI model, enhancing\nthe reliability and trustworthiness of AI solutions in an industrial setting.\n\n## SSM Architecture\nAt a high level, SSMs comprise a front-end Small Language Model (SLM), an adapter layer in the middle, and a wide range of\nback-end domain-knowledge sources. The SLM itself is a small, efficient, language model, which may be domain-specific or not,\nand may have been distilled from a larger model. Thus, domain knowledge may come from either, or both, the SLM and the backends.\n\n\n![High-Level SSM Architecture](./diagrams/ssm-key-components.drawio.png)\n\nThe above diagram illustrates the high-level architecture of an SSM, which comprises three main components:\n\n1. Small Language Model (SLM): This forms the communication frontend of an SSM.\n\n2. Adapters (e.g., LlamaIndex): These provide the interface between the SLM and the domain-knowledge backends.\n\n3. Domain-Knowledge Backends: These include text files, documents, PDFs, databases, code, knowledge graphs, models, other SSMs, etc.\n\nSSMs communicate in both unstructured (natural language) and structured APIs, catering to a variety of real-world industrial systems.\n\n![SSM Composability](./diagrams/ssm-composability.drawio.png)\n\nThe composable nature of SSMs allows for easy combination of domain-knowledge sources from multiple models.\n\n## Getting Started\nYou can begin contributing to the OpenSSM project or use our pre-trained SSMs for your industrial projects. See our [Getting\nStarted Guide](link-to-guide) for more information.\n\n## Roadmap\n- Play with SSMs in a hosted SSM sandbox, uploading your own domain knowledge\n- Create SSMs in your own development environment, and integrate SSMs into your own AI apps\n- Capture domain knowledge in various forms into your SSMs\n- Train SLMs via distillation of LLMs, teacher/student approaches, etc.\n- Apply SSMs in collaborative problem-solving AI systems\n\n## Community\nJoin our vibrant community of AI enthusiasts, researchers, developers, and businesses who are democratizing industrial AI\nthrough SSMs. Participate in the discussions, share your ideas, or ask for help on our [Community Forum](link-to-forum).\n\n## Contribute\nOpenSSM is a community-driven initiative, and we warmly welcome contributions. Whether it\'s enhancing existing models,\ncreating new SSMs for different industrial domains, or improving our documentation, every contribution counts. See our\n[Contribution Guide](docs/CONTRIBUTING.md) for more details.\n\n## License\nOpenSSM is released under the [Apache 2.0 License](./LICENSE.md).\n',
    'author': 'ctn',
    'author_email': 'ctn@aitomatic.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
